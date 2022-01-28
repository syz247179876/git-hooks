"""
校验代码风格钩子
上线环境中请去除该钩子文件和对应的pre-commit脚本!
"""

from __future__ import with_statement, print_function
import os
import re
import shutil
import subprocess
import sys
import tempfile

# 选择指定要检测的代码规则代号
select_codes = []

# 忽略的代码检测规则代号
ignore_codes = ["E121", "E122", "E123", "E124", "E125", "E126", "E127", "E128",
                "E129", "E131", "E501"]
# 额外检测配置
overrides = ["--max-line-length=120"]

# 指明项目目录, 手动修改项目的目录
PROJECT_PATH = r"D:\PythonProjects\Project\Python36\Lib\e_rpa"


def system(command: str, **kwargs):
    """
    创建子进程执行command, 通过PIPE与子进程通信
    """
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(command, **kwargs)
    out, err = proc.communicate()
    return out


def check_format() -> bool:
    modified = re.compile(r'^\s*[AM]+\s+(?P<name>.*\.py$)', re.MULTILINE)
    files = system('git status --porcelain').decode()
    files = modified.findall(files)

    args = ['pycodestyle']
    if select_codes and ignore_codes:
        print('Error: select and ignore codes are mutually exclusive')
        sys.exit(1)
    elif select_codes:
        args.append(f'--select={",".join(select_codes)}')
    elif ignore_codes:
        args.append(f'--ignore={",".join(ignore_codes)}')
    args.extend(overrides)
    # args.append('.')
    args.append(' '.join([rf'{PROJECT_PATH}\{file}' for file in files]))
    command = ' '.join(args)
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    output.wait(2)
    if output.poll() != 0:
        # print('代码风格不符合PEP8, 请检查他们。或使用命令 "git commit --no-verify" 跳过检测.')
        print('The code style does not comply with pep8, please check them. Or use the command "git commit --no-'
              'verify" to skip detection')
        # print('不规范如下：')
        print(output.communicate()[0])
        return False
    return True


def main():
    check_state = check_format()
    if check_state:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
