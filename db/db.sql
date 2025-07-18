-- 删除并重建数据库
DROP DATABASE IF EXISTS student_db;
CREATE DATABASE student_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE student_db;

-- 创建 students 表
CREATE TABLE IF NOT EXISTS students (
    id INT NOT NULL AUTO_INCREMENT,
    student_id VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 scores 表
CREATE TABLE IF NOT EXISTS scores (
    id INT NOT NULL AUTO_INCREMENT,
    student_id VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL COMMENT '考试类型：期中/期末/月考',
    score DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (id),
    KEY (student_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入示例学生数据
INSERT INTO students (student_id, name, password) VALUES
('S1001', 'Alice Johnson', 'pass123'),
('S1002', 'Bob Smith', 'pass123'),
('S1003', 'Charlie Brown', 'pass123'),
('S1004', 'Diana Adams', 'pass123'),
('S1005', 'Ethan Clark', 'pass123'),
('S1006', 'Fiona Lee', 'pass123'),
('S1007', 'George Martin', 'pass123'),
('S1008', 'Hannah Davis', 'pass123'),
('S1009', 'Ian Thomas', 'pass123'),
('S1010', 'Julia White', 'pass123'),
('S1011', 'Kevin Harris', 'pass123'),
('S1012', 'Lily Walker', 'pass123'),
('S1013', 'Michael Young', 'pass123'),
('S1014', 'Nina King', 'pass123'),
('S1015', 'Oscar Scott', 'pass123'),
('S1016', 'Paula Green', 'pass123'),
('S1017', 'Quinn Hall', 'pass123'),
('S1018', 'Rachel Baker', 'pass123'),
('S1019', 'Steven Turner', 'pass123'),
('S1020', 'Tina Allen', 'pass123');

-- 插入英语成绩数据
INSERT INTO scores (student_id, subject, type, score) VALUES
('S1001', 'English', 'Monthly', 87.50),
('S1002', 'English', 'Midterm', 78.00),
('S1003', 'English', 'Final', 92.00),
('S1004', 'English', 'Monthly', 85.00),
('S1005', 'English', 'Midterm', 88.50),
('S1006', 'English', 'Final', 91.00),
('S1007', 'English', 'Monthly', 76.75),
('S1008', 'English', 'Midterm', 83.00),
('S1009', 'English', 'Final', 79.50),
('S1010', 'English', 'Monthly', 90.00);
