# API 项目说明

## 项目概述
本项目是一个基于 Flask 的 API 服务，旨在提供学生数据的集中管理功能。支持通过 Excel 文件批量更新数据，并提供 RESTful 接口对学生数据进行增删改查操作。

## 核心功能
- **Excel 文件上传**：支持通过 API 上传 Excel 文件，批量更新学生数据。
- **学生数据管理**：提供 RESTful 接口对学生数据进行增删改查操作。
- **成绩管理**：支持对学生成绩和学科信息的管理。
- **用户登录**：实现用户认证功能，确保数据安全性。

## 目录结构
```
.
├── app
│   ├── login
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── score
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── students
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── upload
│   │   ├── __init__.py
│   │   └── routes.py
│   └── utility
│       ├── __init__.py
│       ├── database.py
│       ├── routes.py
│       └── student.py
├── db
│   └── db.sql
├── config.py
├── factory.py
├── readme.md
├── resume.md
└── run.py
```

## 模块说明
- **app**: 主要的功能模块，包含登录、成绩管理、学生管理、文件上传等功能。
  - `login`: 用户登录相关逻辑。
  - `score`: 成绩管理模块。
  - `students`: 学生信息管理模块。
  - `upload`: 文件上传处理模块。
  - `utility`: 工具类模块，包含数据库操作和学生相关的工具函数。
- **db**: 数据库相关文件。
  - `db.sql`: 数据库脚本，用于初始化数据库表。
- **config.py**: 配置文件，包含数据库连接信息等。
- **factory.py**: 应用工厂模式实现，用于创建 Flask 应用实例并加载配置。
- **run.py**: 应用启动入口文件。
- **readme.md**: 项目说明文档。
- **resume.md**: 个人简历文件。

## 使用说明
1. **启动应用**：运行 `run.py` 文件。
2. **上传 Excel 文件**：通过指定的 API 接口上传 Excel 文件以更新学生数据。
3. **使用 curl 命令**：对学生数据进行增删改查操作。

## 数据库配置
- 数据库连接信息在 `config.py` 中配置。
- 使用 `db.sql` 脚本初始化数据库表。

## 注意事项
- 确保已安装所有依赖项。
- 在上传 Excel 文件前，请确保文件格式正确。
- 使用 curl 命令时，请确保参数传递正确。

👉 [查看个人简历（resume.md）](./resume.md)


# Jenkins 安装指南 (Ubuntu Linux)

## 安装步骤

1. 添加官方仓库密钥和源：
```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
优化APT下载速度（可选）：

bash
echo 'Acquire::http::Pipeline-Depth "10";' | sudo tee /etc/apt/apt.conf.d/90http-pipeline
echo 'Acquire::http::No-Cache true;' | sudo tee -a /etc/apt/apt.conf.d/90http-pipeline
安装Jenkins：

bash
sudo apt-get update
sudo apt-get install jenkins
基本管理命令
启动服务：sudo systemctl start jenkins
停止服务：sudo systemctl stop jenkins
查看状态：sudo systemctl status jenkins
查看初始密码：sudo cat /var/lib/jenkins/secrets/initialAdminPassword
访问Jenkins
确保防火墙允许8080端口：

bash
sudo ufw allow 8080
sudo ufw enable
在浏览器访问：http://<服务器IP>:8080
注意事项
安装完成后会自动创建jenkins用户和组
服务配置文件位于：/etc/default/jenkins
数据目录位于：/var/lib/jenkins