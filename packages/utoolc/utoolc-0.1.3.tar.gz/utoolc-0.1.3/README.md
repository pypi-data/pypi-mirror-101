# PyJustToolc

> PyJustToolc(utoolc)

```markdown
__________            ____.               __ ___________           .__          
\______   \___.__.   |    |__ __  _______/  |\__    ___/___   ____ |  |   ____  
 |     ___<   |  |   |    |  |  \/  ___/\   __\|    | /  _ \ /  _ \|  | _/ ___\ 
 |    |    \___  /\__|    |  |  /\___ \  |  |  |    |(  <_> |  <_> )  |_\  \___ 
 |____|    / ____\________|____//____  > |__|  |____| \____/ \____/|____/\___  >
           \/                        \/                                      \/                                                                          
                            __                .__          
                     __ ___/  |_  ____   ____ |  |   ____  
                    |  |  \   __\/  _ \ /  _ \|  | _/ ___\ 
                    |  |  /|  | (  <_> |  <_> )  |_\  \___ 
                    |____/ |__|  \____/ \____/|____/\___  >
                                        \/ 
                               Full Of ❤Love❤                                                           
```

banner生成网址:
> http://patorjk.com/software/taag/#p=testall&f=Graffiti&t=PyJustToolc

> http://patorjk.com/software/taag/#p=testall&f=Graffiti&t=utoolc

## fork me
ahviplc/PyJustToolc: ❤PyJustToolc(utoolc) > Python Tools For U (You)❤
> https://github.com/ahviplc/PyJustToolc

PyJustToolc: ❤PyJustToolc(utoolc) > Python Tools For U (You)❤
> https://gitee.com/ahviplc/PyJustToolc

## pypi
### Maintainers

Profile of ahviplc · PyPI
> https://pypi.org/user/ahviplc/

### project

utoolc · PyPI
> https://pypi.org/project/utoolc/

### libraries.io
utoolc 0.1.1 on PyPI - Libraries.io
> https://libraries.io/pypi/utoolc

## who is who
> 我的Java语言的JustToolc项目地址:

```markdown
ahviplc/JustToolc: ❤JustToolc > Java Tools For U (You) ❤
https://github.com/ahviplc/JustToolc

JustToolc: ❤JustToolc > Java Tools For U (You) ❤
https://gitee.com/ahviplc/JustToolc
```

> 我的Go语言的GoJustToolc项目地址:

```markdown
ahviplc/GoJustToolc: ❤GoJustToolc > Go Tools For U (You) ❤
https://github.com/ahviplc/GoJustToolc

GoJustToolc: ❤GoJustToolc > Go Tools For U (You) ❤
https://gitee.com/ahviplc/GoJustToolc
```

## slogan
```markdown
❤PyJustToolc(utoolc) > Python Tools For U (You)❤
```

## 如何使用？

> 安装导入,即可使用.

### 安装包
1. Via pip(recommend):
> pip install utoolc

1.1 官方镜像 pip:
> pip install utoolc -i https://pypi.org/simple/

1.2 阿里云镜像 pip:
> pip install utoolc -i https://mirrors.aliyun.com/pypi/simple/

2. Via easy_install:
> easy_install utoolc

3. From source:
> python setup.py install

从gitee拉取源码
> git clone https://gitee.com/ahviplc/PyJustToolc.git

从github拉取源码
> git clone https://github.com/ahviplc/PyJustToolc.git

从github拉取源码 加速源拉取
> git clone https://hub.fastgit.org/ahviplc/PyJustToolc.git

cd PyJustToolc 进入项目根目录

执行上述命令
> python setup.py install

或者从 https://pypi.org/project/utoolc/0.1.2/#files 从 https://pypi.org/project/utoolc/#files 下载最新版本 下载安装
将下载的【utoolc-0.1.2.tar.gz】解压 执行上述命令
> python setup.py install

4. From source(whl) - 自己下载 *.whl 用以下命令手动安装:
> pip install *.whl

例如:从 https://pypi.org/project/utoolc/0.1.2/#files 从 https://pypi.org/project/utoolc/#files 下载最新版本 下载安装
> pip install utoolc-0.1.2-py3-none-any.whl

#### utoolc依赖的第三方包,第三方模块
> 备注:本项目有依赖的第三方包,第三方模块

> 提醒以下:如果使用 3. From source: 方式安装 则必须自己手动安装相关依赖
一次性安装;

> 提醒以下:如果使用 4. From source(whl) 则不需要,会自动拉取所需依赖并且自动安装.

> 使用requirements.txt安装类库 进行一次性安装

使用官方镜像 pip
> pip install -r requirements.txt

使用阿里云镜像 pip
> pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

> 如果你不想手动安装所需依赖,没关系,安装utoolc包(从pypi上或者手动使用*.whl安装)的时候,会自动安装所需依赖,因为已在setup.py中配置了.

setup.py:31
```markdown
install_requires = [
    'psutil>=5.8.0',
    'requests>=2.25.1',
    'twine>=3.4.1',
    'wheel>=0.36.2',
]
```

> 三方包的说明如下
```markdown
把包上传pypi使用-Twine is a utility for publishing Python packages on PyPI.
twine 
> https://pypi.org/project/twine/

打包使用-This library is the reference implementation of the Python wheel packaging standard, as defined in PEP 427(https://www.python.org/dev/peps/pep-0427/).
It has two different roles:
1. A setuptools extension for building wheels that provides the bdist_wheel setuptools command
2. A command line tool for working with wheel files
It should be noted that wheel is not intended to be used as a library, and as such there is no stable, public API.
wheel
> https://pypi.org/project/wheel/

一款用Py写的跨平台的过程和系统监控库-Cross-platform lib for process and system monitoring in Python
> https://pypi.org/project/psutil/
```

### 使用包
```python
import utoolc

if __name__ == '__main__':
    # 使用 utoolc.do 统一使用入口 当然其他入口也开放 自由发挥
    utoolc.do.utils.print_a_line()
    print(utoolc.do.get_num_cpu())
    print(utoolc.do.get_random.get_random_str_with_counts(3))
    print(utoolc.do.get_os())
    print(utoolc.do.is_mac_os())
    print(utoolc.do.is_win_os())
    print(utoolc.do.is_linux_os())
    print(utoolc.do.get_num_cpu())
    utoolc.do.utils.print_a_line()
```

## 打包上传发布Py模块

> 打包发布Py模块,打包并上传到PyPI

### 快速一览

常用一次性执行sdist和bdist_wheel和bdist --formats=zip三个 打包生成一个源码包*.tar.gz和一个*.whl和一个*.zip即可
> python setup.py sdist bdist_wheel bdist --formats=zip

Only one sdist may be uploaded per release.
所以一次性执行sdist和bdist_wheel,打包生成一个源码包*.tar.gz和一个*.whl
再使用twine进行上传
> python setup.py sdist bdist_wheel

上传pypi

> twine upload dist/*

> python -m twine upload --repository-url https://upload.pypi.org/legacy/  dist/*

### 具体步骤
```markdown
1. 打包和安装第三方包的工具
我们需要借助setuptools和pip和wheel和twine等工具进行自己包的打包和发布以及安装，如果需要构建成wheel还需要安装wheel模块
如果python版本>=2.7.9或者>=3.4，setuptools和pip是已经安装好的，可能需要进行更新到最新版本
> pip install -U pip setuptools wheel

wheel需要安装
> pip install wheel

twine需要安装
> pip install twine

可以使用包管理工具，例如
> yum install pip
> sudo apt-get install pip

2. 具体一些文件介绍
setup.py
这个文件是打包整个项目最重要的文件，它里面提供了两个主要的功能：

setup()函数，此函数的参数指定了如何配置自己的项目。
命令行工具，包括打包，测试，发布等。可以通过下面的命令查看
查看setup.py工具的帮助信息,如下指令
> python setup.py --help-commands

编译python的包(本质上是新建了一个build目录，而后将指定的packages列表包下的所有".py"文件拷贝过去)
> python setup.py build

将源文件进行打包操作
> python setup.py sdist

基于我们刚刚打包的文件进行安装
> pip install .\dist\utoolc-0.1.0.tar.gz 

卸载咱们刚刚安装的包
> pip uninstall utoolc

setup.cfg
此文件包含了构建时候的一些默认参数例如构建bdist_wheel的时候的--universal参数
--universal的意思是这个二进制包对所有 支持的 Python 版本和 ABI（应用程序二进制接口） 都适用，「 一处打包，到处使用」，
生成的文件名类似：*.whl
[bdist_wheel]
universal=1
这样每次打包的时候就会默认使用--universal参数了，效果类似：
打whl包指令如下:
> python setup.py bdist_wheel --universal

README.md
不用多说

utoolc/
此文件夹就是utoolc源代码所在的包。

tests/
此文件夹是一个测试包，包含了一些测试。
```

### setup()的参数
```markdown
setup()的参数

这里只介绍我使用的几个参数，其他参数的具体使用可以参考：https://docs.python.org/3/distutils/setupscript.html

name

versions = "utoolc"
是整个项目的名字，打包后会使用此名字和版本号。

version

from vaspy import __version__
version = __version__
description

是一个简短的对项目的描述，一般一句话就好，会显示在pypi上名字下端。

long_description

是一个长的描述，相当于对项目的一个简洁，如果此字符串是rst格式的，PyPI会自动渲染成HTML显示。这里可以直接读取README.rst中的内容。

url

包的连接，通常为GitHub上的链接或者readthedocs的链接。

packages

需要包含的子包列表，setuptools提供了find_packages()帮助我们在根路径下寻找包，这个函数distutil是没有的。

setup_requires

这个参数定义了VASPy安装和顺利运行所需要的其他依赖项（最基本的），使用pip安装的时候会对这些依赖项进行安装。
关于这个参数与requirements.txt的区别可以参考：install_requires vs Requirements files

classifier

这个参数提供了一系列的分类，在PyPI上会将其放入不同的目录中讲项目进行归类。
具体的categories的名称和规则参考：https://pypi.python.org/pypi?%3Aaction=list_classifiers

test_suite

这个参数可以帮助我们使用
> python setup.py test
来跑单元测试，再也不需要单独再写一个脚本例如utoolc_test.py这样来跑单元测试了
```

### 扩展-bdist命令
> bdist命令是一个二进制分发包，或称作安装程序。该命令可以生成模板操作系统的安装程序。

```markdown
制作windows下的安装包
python setup.py bdist_wininst  # 创建"*.exe"的文件
python setup.py bdist_msi  # 创建"*.msi"的文件 可用
python setup.py bdist --formats=msi  # 同样是创建"*.msi"的文件

制作rpm包
> python setup.py bdist_rpm  # 创建"*.rpm"的文件，该命令需要在Linux操作系统上执行！
> python setup.py bdist --formats=rpm  # 同上

制作压缩文件
> python setup.py bdist --formats=zip  # 创建"*.zip"压缩文件
> python setup.py bdist --formats=gztar  # 创建"*.tar.gz"文件
其中
> python setup.py bdist --formats=zip  等价于  python setup.py sdist
```

### 将python打包成egg包或者whl包(本质上是一个zip文件)
```markdown
安装wheel模块
> pip install wheel

整理好"setup.py"文件

打包whl和egg格式
> python setup.py bdist_egg  # 打"*.egg"的包
> python setup.py bdist_wheel  # 打"*.whl"的包

一次性执行sdist和bdist_wheel两个 生成一个源码包*.tar.gz和一个*.whl即可
> python setup.py sdist bdist_wheel  # 打"*.tar.gz 和 *.whl的包
```

### 上传到pypi
```markdown
> twine upload dist/*

twine 安装： 
> pip install twine

twine 提示输入 pypi 账号和密码，上传成功否就能在自己的pypi账号中看到了。

当你有新版本的时候，你可以使用以下命令 来忽略已经存在的库
> twine upload --skip-existing dist/* 
```

### 添加了 setup.cfg 和 MANIFEST.in
setup.cfg
> 参考了自己打的源码包 直接拿来用了 也可参考别人以后完善它 https://github.com/dabeaz/curio/blob/master/setup.cfg
```text
[egg_info]
tag_build = 
tag_date = 0
```

MANIFEST.in
> 参考了 https://github.com/dabeaz/curio/blob/master/MANIFEST.in
```text
recursive-include examples *
recursive-include docs *
recursive-include tests *
recursive-exclude __pycache__ *.pyc *.pyo
include README.rst
include README.md
```

## 待完善,待复看
```markdown
packages=find_packages(where='PyJustToolc', include=('utoolc','example'),exclude=("*.tests", "*.tests.*", "tests.*", "tests")), # include all packages under automated

long_description = """
=====
❤PyJustToolc(utoolc) > Python Tools For U (You)❤
=====
------------
1. Via pip(recommend)::
    pip install utoolc
2. Via easy_install::
    easy_install utoolc
3. From source::
    python setup.py install
If you want to use **mayavi** to visualize VASP data, it is recommened to install `Canopy environment <https://store.enthought.com/downloads/#default>`_ on your device instead of installing it manually.
After installing canopy, you can set corresponding aliases, for example:
.. code-block:: shell
    alias canopy='/Users/<yourname>/Library/Enthought/Canopy/edm/envs/User/bin/python'
    alias canopy-pip='/Users/<yourname>/Library/Enthought/Canopy/edm/envs/User/bin/pip'
    alias canopy-ipython='/Users/<yourname>/Library/Enthought/Canopy/edm/envs/User/bin/ipython'
    alias canopy-jupyter='/Users/<yourname>/Library/Enthought/Canopy/edm/envs/User/bin/jupyter'
Then you can install utoolc to canopy::
    canopy-pip install utoolc
"""
```

### .pypirc
> 下面为.pypirc内容
```text
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository: https://upload.pypi.org/legacy/
username: ahviplc
password: ###

[pypitest]
repository: https://test.pypi.org/legacy/
username: ahviplc
password: ###
```

## 一些链接
```markdown
Python __all__变量用法
http://c.biancheng.net/view/2401.html

打包发布Python模块的方法详解_python_脚本之家 - 此打包根据这个做的
https://www.jb51.net/article/92789.htm
||
GitHub - PytLab/VASPy: Manipulating VASP files with Python.
https://github.com/PytLab/VASPy

Python的打包工具(setup.py)实战篇 - 尹正杰 - 博客园 - 还有这个 - 很不错,很全
https://www.cnblogs.com/yinzhengjie/p/14124623.html

手把手教你打包Python库并创建自己的PyPI项目 - 简书 - 也可参考
https://www.jianshu.com/p/6019aee27883
||
GitHub - YaokaiYang-assaultmaster/py3PortScanner: 🎃Port scanner for Python >= 3.0! Faster! Stronger! Better!
https://github.com/YaokaiYang-assaultmaster/py3PortScanner

Python打包指南2021 | Frost's Blog
https://frostming.com/2020/12-25/python-packaging/

使用 twine 上传自己的 python 包到 pypi - leffss - 博客园
https://www.cnblogs.com/leffss/p/12029963.html

GitHub - pypa/twine: Utilities for interacting with PyPI
https://github.com/pypa/twine

GitHub - pdm-project/pdm: A modern Python package manager with PEP 582 support.
https://github.com/pdm-project/pdm

PyPI · The Python Package Index 正式
https://pypi.org/

TestPyPI · The Python Package Index 测试
https://test.pypi.org/

Python包管理工具setuptools之setup函数参数详解 - 一切都是当下 - 博客园
https://www.cnblogs.com/potato-chip/p/9106225.html

Python编程：将markdown格式转换为rst格式_彭世瑜的博客-CSDN博客 - 可用的
https://blog.csdn.net/mouday/article/details/81876270

CloudConvert - rst和md互转 在线网站 - 不会写rst,可先写成md,再转成rst使用 - 可用的
https://cloudconvert.com/

python发布包到pypi的踩坑记录 -配置【.pypirc】- rongpmcu - 博客园
https://www.cnblogs.com/rongpmcu/p/7662821.html

Docverter
https://docverter.com/

Docverter/docverter: Docverter Server
https://github.com/docverter/docverter

msabramo/pydocverter: Python client for Docverter service (pandoc as a service)
https://github.com/msabramo/pydocverter

Docverter/docverter-ruby: The official Docverter Ruby SDK
https://github.com/docverter/docverter-ruby

Python setup.py和MANIFEST.in文件
https://blog.csdn.net/fragmentalice/article/details/44833013

关于python中的setup.py
https://blog.csdn.net/xluren/article/details/41114779

做PYTHON项目需要一个MANIFEST.IN，它应该是什么？
http://www.dovov.com/pythonmanifest-in.html

2. Writing the Setup Script — Python 3.9.4 documentation
https://docs.python.org/3/distutils/setupscript.html

2. Writing the Setup Script — Python 3.9.4 documentation
https://docs.python.org/3/distutils/setupscript.html#other-options

9. API Reference — Python 3.9.4 documentation - 里面有 packages 等的参数使用说明
https://docs.python.org/3/distutils/apiref.html#distutils.core.setup

python-aiplatform/setup.py at master · googleapis/python-aiplatform · GitHub - 里面的【platforms="Posix; MacOS X; Windows",】
https://github.com/googleapis/python-aiplatform/blob/master/setup.py

Docutils: Documentation Utilities
https://docutils.sourceforge.io/
```

## about me
```markdown
By LC
寄语:一人一世界,一树一菩提!~LC
Version 0.1.0 From 2021
```
