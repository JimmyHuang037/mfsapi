# 项目设计文档

## 项目概述
本项目是一个学生信息管理系统，旨在提供全面的学生信息与成绩管理功能。主要功能包括：
- 提供 RESTful Web API 接口，实现学生数据的增删改查操作。
- 支持通过 Excel 文件批量导入学生基础信息。
- 对学生成绩进行细致管理，涵盖添加、修改、删除和查询成绩等操作。
- 提供登录认证功能，验证学生身份并返回对应学生信息与成绩。

## 技术栈
- **后端**：采用 Python 语言结合 Flask 框架开发，借助 Flask 轻量级、灵活的特性构建高效的 Web API。
- **数据库**：使用 MySQL 作为数据存储系统，保障数据的持久化与一致性。
- **前端**：运用基础的 HTML、CSS 和 JavaScript 实现简单的用户交互界面。
- **其他工具**：
  - `pandas` 库：用于处理 Excel 文件的读取与解析，实现学生数据的批量导入。
  - `Flask - CORS` 扩展：解决跨域请求问题，方便前后端分离开发。
  - `mysql - connector - python` 库：实现 Python 与 MySQL 数据库的稳定连接与数据交互。

## 文件结构
```bash
.
├── .git/                   # Git 版本控制目录
├── .gitignore              # 配置 Git 需忽略的文件和目录
├── .vscode/                # VS Code 编辑器配置目录
├── app/
│   ├── __init__.py         # 初始化 Flask 应用，配置数据库连接、CORS 并注册蓝图
│   ├── api/                # API 接口相关目录
│   ├── core/               # 核心功能模块目录
│   ├── main/
│   │   └── routes.py       # 主路由逻辑文件
│   ├── models/
│   │   └── student.py      # 学生模型类及数据库操作方法
│   └── services/           # 业务逻辑服务目录
├── app.py                  # 主应用程序入口文件，负责启动 Flask 应用
├── docs/
│   ├── app_design.md       # 项目设计文档（当前文件）
│   └── db_desing.md        # 数据库设计相关文档
├── readme.md               # 项目说明文档，介绍项目基本信息和使用方法
├── requirements.txt        # 项目依赖包列表，记录项目运行所需的 Python 库及其版本