<!--
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-10 13:32:41
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-16 16:11:16
 * @FilePath: /store/README.md
 * @Description: README.md
-->
# 内网应用商店
## 项目简介
本项目是基于Python开发的内网私有化应用商店系统，专为企业/组织内网环境设计，解决内部应用分发、版本管理、权限控制、安装统计等核心需求，支持Windows/Linux/macOS多终端内网访问，无需对接公网应用市场，保障内部应用分发的安全性和可控性。

### 核心特性
- 应用管理：支持内部应用的上传、版本迭代、上下架、分类管理（如办公工具、开发工具、业务系统）；
- 权限控制：基于角色的权限管理（超级管理员/普通管理员/普通用户），可限制用户/部门可见应用；
- 下载安装：提供一键下载、内网静默安装（支持exe/msi/deb/rpm等格式），记录下载/安装日志；
- 版本回滚：支持应用历史版本查询、回滚，可标记“推荐版本”“稳定版本”；
- 统计分析：可视化展示应用下载量、安装量、活跃用户，支持按时间/部门维度筛选；
- 内网适配：无公网依赖，支持内网IP访问、域名映射，适配企业内网防火墙规则；
- 消息通知：应用更新、上下架时自动推送通知至内网用户端。

## 技术栈
- Python版本：3.13.x（推荐，兼容多系统内网环境）
- 核心框架/依赖：
  - Web框架：Flask 2.3.3（轻量易部署，适配内网低资源服务器）
  - 数据库：SQLite（默认，轻量免部署）/MySQL 8.0（企业级内网部署）
  - 前端：Bootstrap 5.3 + jQuery（适配内网低版本浏览器）
  - 文件存储：本地文件系统（内网服务器目录）/MinIO（内网对象存储，可选）
  - 权限认证：Flask-Login + Flask-Principal
  - 日志：logging（记录操作/访问/错误日志）
  - 可视化：ECharts 5.4（下载/安装数据可视化）
  - 其他：requests（内网接口调用）、pyinstaller（可选，打包客户端）、psutil（监控服务器资源）

## 快速开始（内网部署）
### 前置条件
1. 内网服务器要求：
   - 系统：Linux/CentOS 7+/Windows Server 2016+（推荐Linux，稳定性更高）
   - 网络：服务器配置固定内网IP（如192.168.1.100），确保内网终端可访问；
   - 依赖：服务器安装Python3.9.x，关闭内网防火墙限制（或开放指定端口，默认5000）。
2. 客户端要求：内网终端（Windows/Linux/macOS）可访问服务器内网IP。

### 部署步骤
#### 1. 拉取/上传项目至内网服务器
```bash
# 若内网服务器可访问代码仓库（如GitLab内网仓库）
git clone http://192.168.1.99/xxx/intranet-app-store.git
# 若无内网仓库，直接将项目压缩包上传至服务器并解压
unzip intranet-app-store.zip -d /opt/intranet-app-store


/media/wangye/DATA1/Projects/static/store/  # 源根目录
├── dists/
│   └── uos/                     # 发行版名称
│       ├── wangye/                 # 组件名称
│       │   └── binary-arm64/       # 架构目录（你的 arm64 系统）
│       │       ├── Packages        # 包索引（明文）
│       │       ├── Packages.gz     # 包索引（压缩）
│       │       └── Packages.bz2    # 包索引（压缩，可选）
│       ├── Release                 # 源索引文件（必需）
└── pool/
    └── main/                       # 对应组件 main
        └── [包名首字母]/            # 按包名首字母分类
            └── xxx.deb             # rm64 架构 deb 包



python3-pymysql
python3-dotenv
python3-requests
python3-pyqt5
python3-pyqt5.qtwebkit


sudo pip3 install pyqt5==5.15.7
sudo pip3 install pymysql==1.0.2 python-dotenv==0.21.1 requests==2.28.2