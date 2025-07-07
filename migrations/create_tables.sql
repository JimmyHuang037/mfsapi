-- 学生表（主键改为自增id，保留student_id作为唯一键）
CREATE TABLE IF NOT EXISTS students (
    id INT NOT NULL AUTO_INCREMENT,
    student_id VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 成绩表（新增type字段）
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