import pandas as pd

import mysql.connector
from sqlalchemy import create_engine

# 读取Excel文件
excel_data = pd.read_excel('ns.xlsx')

db_connection = mysql.connector.connect(
    host="localhost",      # 直接指定主机
    user="root",           # 直接指定用户名
    password="Newuser1",   # 直接指定密码
    database="student_db"  # 直接指定数据库名
)


# 创建游标对象
cursor = db_connection.cursor()

# 批量插入数据
for index, row in excel_data.iterrows():
    placeholders = ', '.join(['%s'] * len(row))
    columns = ', '.join(row.index)
    sql = f"INSERT INTO students ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(row))

# 提交事务
db_connection.commit()

# 关闭连接
cursor.close()
db_connection.close()