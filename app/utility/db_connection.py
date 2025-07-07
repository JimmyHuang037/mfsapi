import mysql.connector
from config import Config

def get_db_connection():
    """获取数据库连接"""
    config = Config()
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
