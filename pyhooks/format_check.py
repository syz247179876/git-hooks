"""
校验代码风格钩子
author: syz
date: 2022/1/24
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


def system(command, **kwargs):
    """
    创建子进程执行command, 通过PIPE与子进程通信
    """
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(command, **kwargs)
    out, err = proc.communicate()
    return out


def main():
    modified = re.compile(r'^\s*[AM]+\s+(?P<name>.*\.py$)', re.MULTILINE)
    files = system('git status --porcelain').decode()
    files = modified.findall(files)

    tempdir = tempfile.mkdtemp()
    for name in files:
        filename = os.path.join(tempdir, name)
        filepath = os.path.dirname(filename)

        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(filename, 'w') as f:
            system(f'git show :{name}', stdout=f)
    args = ['pycodestyle']
    if select_codes and ignore_codes:
        print('Error: select and ignore codes are mutually exclusive')
        sys.exit(1)
    elif select_codes:
        args.append(f'--select={",".join(select_codes)}')
    elif ignore_codes:
        args.append(f'--ignore={",".join(ignore_codes)}')
    args.extend(overrides)
    args.append('.')
    command = ' '.join(args)
    print(command)
    output: str = system(command, cwd=tempdir)
    shutil.rmtree(tempdir)
    if output:
        print('代码风格不符合PEP8, 请检查他们。或使用命令 "git commit --no-verify" 跳过检测.')
        print('不规范代码如下：')
        print(output.decode())
        sys.exit(1)


if __name__ == '__main__':
    main()
