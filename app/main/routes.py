from flask import Blueprint
from flask_cors import CORS

main_bp = Blueprint('main', __name__)

# 数据库配置
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Newuser1'
DB_NAME = 'student_db'

# 创建数据库连接
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# 初始化数据库
def init_db():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        with open('migrations/create_tables.sql', 'r') as f:
            sql_file = f.read()
        sql_commands = sql_file.split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
        conn.commit()
        cursor.close()
        conn.close()