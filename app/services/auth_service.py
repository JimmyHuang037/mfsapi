from app.utility.db_connection import get_db_connection
from flask import current_app

def authenticate_user(student_id, password):
    """
    验证用户身份
    :param student_id: 学号
    :param password: 密码
    :return: 若验证成功返回学生信息，失败返回 None
    """
    try:
        with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT student_id, password FROM students 
                WHERE student_id = %s AND password = %s
            """, (student_id, password))
            return cursor.fetchone()
    except Exception as e:
        current_app.logger.error(f"Database error during authentication: {str(e)}")
        return None
