# API 项目说明

## 功能概述
- 提供 Excel 文件上传功能，用于更新学生数据。
- 支持使用 curl 命令发起对学生数据的增删改查请求。
- 数据库中存储了所有学生数据，包括学科和分数。

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
│   │   ├── routes.py
│   │   └── students.py
│   ├── upload
│   │   ├── __init__.py
│   │   └── routes.py
│   └── utility
│       ├── __init__.py
│       ├── database.py
│       ├── routes.py
│       └── student.py
├── db
│   ├── create_tables.sql
│   └── schema.sql
├── app.py
├── config.py
├── factory.py
└── readme.md
```

## 模块说明
- **app**: 主要的功能模块，包含登录、成绩管理、学生管理、文件上传等功能。
  - `login`: 用户登录相关逻辑。
  - `score`: 成绩管理模块。
  - `students`: 学生信息管理模块。
  - `upload`: 文件上传处理模块。
  - `utility`: 工具类模块，包含数据库操作和学生相关的工具函数。
- **db**: 数据库相关文件。
  - `create_tables.sql`: 创建数据库表的 SQL 脚本。
  - `schema.sql`: 数据库模式定义。
- **app.py**: 应用入口文件。
- **config.py**: 配置文件。
- **factory.py**: 应用工厂模式实现，用于创建 Flask 应用实例并加载配置。
- **readme.md**: 项目说明文档。

## 使用说明
1. 启动应用：运行 `app.py` 文件。
2. 上传 Excel 文件：通过指定的 API 接口上传 Excel 文件以更新学生数据。
3. 使用 curl 命令对学生数据进行增删改查操作。

## 数据库配置
- 数据库连接信息在 `config.py` 中配置。
- 使用 `create_tables.sql` 脚本创建数据库表。
- 数据库模式定义在 `schema.sql` 中。

## 注意事项
- 确保已安装所有依赖项。
- 在上传 Excel 文件前，请确保文件格式正确。
- 使用 curl 命令时，请确保参数传递正确。

👉 [查看个人简历（resume.md）](./resume.md)
