# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
# Package meta-data.
NAME = 'iwester-extractor'
VERSION = '1.0.3'
DESCRIPTION = 'A web extractor Python project'
URL = 'https://gitee.com/zhang-chuang/web_extractor'
EMAIL = 'iwester@163.com'
AUTHOR = 'iwester'
REQUIRES_PYTHON = '>=3.6, <4'
REQUIRED = [
    'pyquery==1.4.3'
    'tldextract==3.1.0'
]
# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

setup(
    name=NAME,  # Required 项目的名称
    version=VERSION,  # Required 项目的版本,后续代码有了任何更改，再次上传需要增加版本号
    description=DESCRIPTION,  # 项目的简短描述
    long_description=long_description,  # 项目的详细描述，会显示在PyPI的项目描述页面
    long_description_content_type='text/markdown',  # 用于指定long_description的markup类型
    url=URL,  # 代码仓库的链接
    author=AUTHOR,  # 作者
    author_email=EMAIL,  # 邮件
    keywords='web，extractor',  # Optional
    python_requires=REQUIRES_PYTHON,  # python版本

    # package_dir={'': 'src'},  # Optional
    # packages=find_packages(where='src'),  # Required
    packages=find_packages(),  # 注意这种写法主体代码文件夹名称=项目名称
    # 希望被打包的文件
    include_package_data=True,
    package_data={
        '': ['*.txt']
    },
    # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    data_files=[
        ('my_data', ['data/data_file'])
    ],
    # 不打包某些文件
    exclude_package_data={},
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    install_requires=REQUIRED,  # 当前项目需要的库
    # install_requires 在安装模块时会自动安装依赖包
    # 而 extras_require 不会，这里仅表示该模块会依赖这些包
    # 但是这些包通常不会使用到，只有当你深度使用模块时，才会用到，这里需要你手动安装
    extras_require=EXTRAS,

    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # 该文件入口指向 foo/main.py 的main 函数
    entry_points={
        # 'console_scripts': [
        #     'foo = foo.main:main'
        # ]
    },

    project_urls={  # Optional
        'Source': 'https://gitee.com/zhang-chuang/web_extractor/',
    },
)
