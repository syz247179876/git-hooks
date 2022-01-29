"""
commit的message规范校验钩子
author: syz
使用指南：
https://hexo-syz247179876.vercel.app/2022/01/24/Python%E9%A1%B9%E7%9B%AE%E4%BD%BF%E7%94%A8git%E9%92%A9%E5%AD%90%E7%9A%84%E6%8C%87%E5%8D%97/
"""
import os
import re
import sys

# 指明项目目录, 手动修改项目的目录
PROJECT_PATH = r"D:\PythonProjects\Project\Python36\Lib\e_rpa"

MODIFIED_RELATE_PATH = '.git/COMMIT_EDITMSG'


def check_message(content: str) -> bool:
    """
    commit的message规范性校验, 遵循Angular规范
    """
    pattern = re.compile(r"^(build|ci|docs|feat|fix|pref|refactor|test)(.*?):\s(.){1,88}((.*)\n|\t)*")

    res = pattern.match(content.strip())
    if res:
        return True
    return False


def main(filename: str):
    filepath = os.path.join(PROJECT_PATH, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content: str = f.read()
    check_state = check_message(content)
    if check_state:
        sys.exit(0)
    else:
        print('Your message is not formatted correctly, please start with use the following format:\n\n'
              '------gap-line-------\n'
              'feat(function module): add multiple new functions to the function library\n\n'
              '1.add new function of obtaining the specified region according to the specific region.\n'
              '2.add new function of clearing variable within robot operation.\n'
              '3.optimize code of function of `vague_match`'
              )
        print('------gap-line-------\n')
        print('Last but not least, the format above is a example used English because of Garbled code, while in our '
              'project, we need use Chinese!')
        sys.exit(1)


if __name__ == "__main__":
    # message_file = sys.argv[1]
    main(MODIFIED_RELATE_PATH)
