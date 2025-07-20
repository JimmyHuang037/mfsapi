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