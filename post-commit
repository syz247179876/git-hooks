#!/bin/sh
# author: syz

# python的虚拟路径和项目路径
INSTALL_PYTHON='D:\pythonprojects\pyautoguis\scripts\python.exe'
PROJECT_PATH="D:\PythonProjects\Project\Python36\Lib\e_rpa"
USER_NAME=$(git config user.name)

# 进入虚拟环境
SCRIPTS_PATH=$(cd `dirname ${INSTALL_PYTHON}`; pwd)
VIRTUAL_PATH="${SCRIPTS_PATH}/activate"
source $VIRTUAL_PATH

# PIP路径
PIP_PATH="${SCRIPTS_PATH}\pip"

# 模块inspect
# BASE_PATH=$(cd `dirname $0`; pwd)
# PROJECT_PATH=$(cd `dirname $BASE_PATH`; pwd)

# 执行1
cd $PROJECT_PATH
$INSTALL_PYTHON "${PROJECT_PATH}\git_hook\inspect_modules.py"

echo $?

# commit and push package.zip
#PACKAGE_PATH="${PROJECT_PATH}\package/${USER_NAME}"
#echo $PACKAGE_PATH
#git add $PACKAGE_PATH
#git commit -m "upload module package" $PACKAGE_PATH

echo "package has been added and committed, don't forget push!"
