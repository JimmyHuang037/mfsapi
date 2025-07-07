# 数据库设计文档

## 数据库概述

本项目使用MySQL数据库，主要包含两个表：
- `students` 表：存储学生基本信息
- `scores` 表：存储学生成绩信息

## 表结构设计

### students 表

#### 字段定义
| 字段名       | 类型         | 约束条件                | 说明       |
|------------|------------|---------------------|----------|
| id         | int        | PRIMARY KEY, AUTO_INCREMENT | 主键       |
| student_id | varchar(50) | NOT NULL, UNIQUE      | 学号       |
| name       | varchar(100)| NOT NULL              | 姓名       |
| password   | varchar(100)| NOT NULL              | 密码       |

#### 表约束
- `student_id` 字段具有唯一性约束，确保学号不重复
- 所有字段均为非空约束

### scores 表

#### 字段定义
| 字段名       | 类型          | 约束条件                     | 说明           |
|------------|-------------|--------------------------|--------------|
| id         | int         | PRIMARY KEY, AUTO_INCREMENT | 主键           |
| student_id | varchar(50) | NOT NULL                 | 外键，关联students表 |
| subject    | varchar(100) | NOT NULL                 | 科目           |
| type       | varchar(50)  | NOT NULL                 | 成绩类型（如平时、期中、期末） |
| score      | decimal(5,2) | NOT NULL                 | 分数           |

#### 表约束
- `student_id` 字段为外键，引用 `students(student_id)`
- 所有字段均为非空约束

## 关系图

```mermaid
erDiagram
    students ||--o{ scores : "1..N"
    students {
        int id
        varchar(50) student_id
        varchar(100) name
        varchar(100) password
    }
    scores {
        int id
        varchar(50) student_id
        varchar(100) subject
        varchar(50) type
        decimal(5,2) score
    }
```

## 数据库特点

1. **规范化设计**：通过主外键关系实现数据规范化，减少数据冗余
2. **数据完整性**：通过非空约束和唯一性约束保证数据完整性
3. **扩展性**：支持轻松添加新的成绩类型和科目
4. **安全性**：学生密码存储采用加密方式（虽然当前实现中未体现）

## 注意事项

1. 在导入Excel数据时，需要确保数据格式与数据库结构一致
2. 对于大量数据导入操作，建议使用批量插入技术提高效率
3. 需要定期对数据库进行备份以防止数据丢失