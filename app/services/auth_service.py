from app.utility.db_connection import get_db_connection
from flask import current_app

def authenticate_user(student_id, password):
    try:
        with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
            # 修改查询语句，确保返回name字段
            cursor.execute(
                "SELECT student_id, name FROM students WHERE student_id = %s AND password = %s",
                (student_id, password)
            )
            student = cursor.fetchone()
            return student if student else None
    except Exception as e:
        current_app.logger.error(f"Authentication error for student {student_id}: {str(e)}")
        return None

