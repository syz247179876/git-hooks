# git-hooks

基于Python和Shell的git的钩子

git hooks with Python and Shell.

本项目编写的钩子的需求来源于工作开发中。

The requirements of the hook written in this project come from the work development.

`format_check` hook
该钩子可用于pre-commit钩子, 提交前检查代码风格及规范是否满足pep8, 不规范的地方将会以文件 + 行号 + 具体不规范的行为描述的形式输出。

This hook can be used in the pre-commit hook to check whether the code style and specification meet pep8 before submission. The non-standard places will be output in the form of file + line number + specific non-standard behavior description.

`inspect_modules` hook
该钩子可用于post-commit钩子, 在整个提交过程完成后运行, 每次commit会自动检测当前开发者是否安装了新的第三方模块或者对第三方模块的版本进行修改。
如果新安装模块或者模块的版本发生修改, 则会在项目根目录, 创建package文件夹, 在团队开发中会为每个开发者单独创建文件夹, 存放待修改的依赖包的源代码, 依赖包树的json文件, 依赖包树扁平后的json文件。

This hook can be used for the post commit hook. It runs after the whole submission process is completed. Each commit will automatically detect whether the current developer has installed a new third-party module or modified the version of the third-party module.
If the newly installed module or the version of the module is modified, a package folder will be created in the project root directory. In team development, a separate folder will be created for each developer to store the source code of the dependent package to be modified, the JSON file of the dependent package tree, and the JSON file after the flat dependent package tree.

注：其中需手动修改`SITE_PACKAGES_PATH`,`PIP_PATH`,`VIRTUAL_ENV`

Note: you need to modify ` site manually_ PACKAGES_ PATH`,`PIP_ PATH`,`VIRTUAL_ ENV`

分别为：

They are:

1.自己虚拟环境或非虚拟环境下Python的site-packages所在目录。

1. The directory of Python site packages in your own virtual environment or non virtual environment.

2.自己虚拟环境或非虚拟环境下Python的pip.exe所在目录。

2. Pip of Python in your own virtual environment or non virtual environment Exe directory.

3.自己虚拟环境激活入口activate所在目录。

3. Activate the directory of your virtual environment activation portal.


`post-commit.sh` hook是一个简单的shell例子, 用于调用inspect_modules的py文件, 实现模块检测。我在shell方面是个新手。

`post-commit. SH ` hook is a simple shell example for calling inspect_ Modules py file to realize module detection. I'm a novice at shell.
