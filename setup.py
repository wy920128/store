#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import sys

# 检查Python版本（确保UOS系统兼容）
if sys.version_info < (3, 8):
    sys.exit("Error: appstore requires Python 3.8 or higher (UOS default is 3.8+)")

# 读取README.md（处理文件不存在的情况）
def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    return "UOS内网应用商店 - 基于PyQt6的卡片式应用商店"

# 项目核心配置
setup(
    name="appstore",
    version="1.0.0",          # 需与debian/changelog中的版本一致
    packages=find_packages(),  # 自动识别appstore目录下的所有Python包
    package_data={
        # 包含项目中的资源文件（如图片、配置等，根据实际目录补充）
        "appstore": [
            "resources/*",    # 若有resources目录（图标/配置），需添加
            "*.ico", "*.png", "*.svg"  # 所有图片资源
        ]
    },
    include_package_data=True,  # 确保资源文件被打包
    install_requires=[
        # 核心依赖（严格匹配你的代码导入）
        "PyQt6>=6.4.0",        # 项目核心UI框架（UOS适配版）
        "PyMySQL>=1.0.0",      # 数据库操作（pymysql）
        "python-dotenv>=1.0.0" # 环境变量配置（dotenv）
    ],
    # 定义可执行命令（UOS终端直接运行appstore即可启动）
    entry_points={
        "console_scripts": [
            "appstore = appstore.layout:main"  # 指向layout.py的main函数
        ],
        # 可选：桌面应用入口（适配UOS桌面）
        "gui_scripts": [
            "appstore-gui = appstore.layout:main"
        ]
    },
    # 项目元信息
    author="王野",
    author_email="18545455617@496.com",
    description="UOS内网应用商店（卡片式布局，自适应UI）",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="",  # 若无项目地址，留空即可
    license="MIT",  # 开源协议（可根据实际修改）
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: Linux :: UOS",  # 明确适配UOS
        "Environment :: X11 Applications :: Qt",     # 指明Qt桌面环境
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment :: File Managers",
    ],
    python_requires=">=3.8",  # UOS默认Python3.8，无需更高版本
    # 可选：安装后的数据文件（如桌面快捷方式、图标）
    data_files=[
        # 桌面快捷方式（配合debian打包使用）
        ("/usr/share/applications", ["debian/appstore.desktop"]),
        # 图标文件（需确保项目中有该文件）
        ("/usr/share/icons/hicolor/64x64/apps", ["appstore/resources/appstore.png"])
    ],
    # 可选：关键字（便于搜索）
    keywords="appstore, 应用商店",
    # 适配UOS的额外配置
    zip_safe=False,
    platforms=["Linux"]
)