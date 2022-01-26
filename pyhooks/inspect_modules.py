"""
模块增量检查钩子
author: syz
"""

import hashlib
import json
import os
import subprocess
import sys
import typing as t
import zipfile
from concurrent.futures.thread import ThreadPoolExecutor


def system(command, **kwargs) -> str:
    """
    创建子进程执行command, 通过PIPE与子进程通信
    """
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(command, **kwargs)
    out, err = proc.communicate()
    out: bytes
    return out.decode()


# 这里手动修改下自己项目所使用的Python全局环境或虚拟环境以及pip路径, 还有包路径
SITE_PACKAGES_PATH = os.path.join(r'D:\PythonProjects\pyautoguis\Lib\site-packages')
PIP_PATH = os.path.join(r'D:\PythonProjects\pyautoguis\Scripts\pip.exe')
VIRTUAL_ENV = os.path.join(r'D:\PythonProjects\pyautoguis\Scripts\activate.bat')

USER_NAME = system('git config user.name').replace('\n', '').strip()
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
PACKAGE_DIR = os.path.join(PROJECT_PATH, 'package')
USER_DIR = os.path.join(PACKAGE_DIR, USER_NAME)
PACKAGE_NAME = f'modified_package'
PACKAGE_PATH = os.path.join(USER_DIR, f'{PACKAGE_NAME}.zip')
PACKAGE_NAME_FLAT = os.path.join(USER_DIR, 'package_name_flat.json')
PACKAGE_NAME_TREE = os.path.join(USER_DIR, 'package_tree.json')
REQUIREMENTS_PATH = os.path.join(PROJECT_PATH, 'requirements.txt')


def compress_zip(
        source_path: t.List,
        aim_path: str,
        package_name: str,
        cypher: str = None,
        reserve: bool = True
) -> bool:
    """
    压缩zip包
    包含压文件+文件夹
    """
    aim_path = os.path.join(aim_path, f'{package_name}.zip')
    with zipfile.ZipFile(aim_path, 'w', zipfile.ZIP_DEFLATED) as f:
        if cypher:
            f.setpassword(cypher)
        for dir_ in source_path:
            if os.path.isfile(dir_):
                f.write(dir_, compress_type=zipfile.ZIP_STORED)
            else:
                for root, dirs, files in os.walk(dir_):
                    for file in files:
                        abs_path = os.path.join(os.path.join(root, file))
                        f.write(abs_path, compress_type=zipfile.ZIP_STORED)
        f.close()
    if not reserve:
        for dir_ in source_path:
            os.remove(dir_)
    return True


class ThreadingPool(object):
    """
    线程池
    """
    instance = None
    pool = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, worker: int = 5):
        if not self.pool:
            self.pool = ThreadPoolExecutor(worker)

    @property
    def thread_pool(self):
        return self.pool

    def close(self, wait: bool = True) -> None:
        if self.pool:
            self.pool.shutdown(wait)


try:
    exec('import pipdeptree')
except ImportError:
    block = os.popen(f'{PIP_PATH} install pipdeptree')
    block.readlines()

# if not os.path.exists(PACKAGE_DIR):
#     os.mkdir(PACKAGE_DIR)
if not os.path.exists(os.path.join(PACKAGE_DIR, USER_NAME)):
    os.makedirs(USER_DIR)

old_module_map = {}
new_module_map = {}


def inspect_content():
    """
    校验是否新增模块或者模块的版本发生变化
    """
    old_cipher = validate_and_generate(old_module_map)
    wait = os.popen(f'{PIP_PATH} freeze > {REQUIREMENTS_PATH}')
    wait.readlines()
    new_cipher = validate_and_generate(new_module_map)
    return old_cipher == new_cipher


def validate_and_generate(module_map: t.Dict) -> str:
    """
    构造映射, 检测发生变化的模块
    """

    with open(REQUIREMENTS_PATH, 'r', encoding='utf-8') as f:
        modules = f.readlines()
        m = hashlib.md5()
        m.update(f.read().encode('utf-8'))

        for module in modules:
            module_list = module.split('==')
            if len(module_list) == 2:
                module_name, module_version = module_list[0], module_list[1].replace('\n', '')
                module_map[module_name] = module_version
    return m.hexdigest()


def search_module():
    """
    严查差异模块, 包含新增模块和版本变化模块
    """
    modified_modules = {}
    for key, value in new_module_map.items():
        if key not in old_module_map or new_module_map[key] != old_module_map[key]:
            modified_modules[key] = value
    return modified_modules


def pack_modified_modules(pool: ThreadPoolExecutor):
    """
    打包被修改的依赖包及其依赖包
        1.构建包依赖树并写入文件
        2.清洗依赖树, 扁平化依赖库, 写入文件
        3.打包所有改变的模块及其依赖
    如果存在压缩包, 则合并两次压缩包
    """
    modified_modules = search_module()
    total_tree_modules = []
    total_flat_modules = {}
    if modified_modules:
        for name, version in modified_modules.items():
            r = os.popen(f'pipdeptree -p {name} -j')
            module_tree: t.List = json.loads(r.read())
            total_tree_modules.append(module_tree)
            clean_tree(module_tree, total_flat_modules)

        pool.submit(write, PACKAGE_NAME_TREE, total_tree_modules)
        pool.submit(write, PACKAGE_NAME_FLAT, total_flat_modules)
        modules_abs_path = [os.path.join(SITE_PACKAGES_PATH, filename) for filename in total_flat_modules.keys()]
        pool.submit(compress_zip, modules_abs_path, USER_DIR, PACKAGE_NAME)


def write(file_path: str, total_data: t.Union[t.Dict, t.List]):
    """
    写入文件
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(total_data, f)


def clean_tree(module_tree: t.List, total_tree_modules: t.Dict):
    """
    清洗模块树, 抽取出模块及版本, 构造已修改的模块及版本文档
    """

    for module in module_tree:
        module: t.Dict
        module_name = module.get('package').get('package_name')
        module_version = module.get('package').get('installed_version')
        total_tree_modules.setdefault(module_name, module_version)
        for dependence in module.get('dependencies'):
            dependence: t.Dict
            total_tree_modules.setdefault(dependence.get('package_name'), dependence.get('installed_version'))


if __name__ == "__main__":
    instance = ThreadingPool(3)
    inspect_content()
    pack_modified_modules(instance.thread_pool)
    instance.close()
    print(f'Module has finished checking, generating package for `{USER_NAME}` \n'
          f'the path is {USER_DIR}!')
    subprocess.run(rf'git add D:\PythonProjects\Project\Python36\Lib\e_rpa\package\{USER_NAME}')
    sys.exit(1)
