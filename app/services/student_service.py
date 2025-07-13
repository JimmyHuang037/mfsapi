from app.utility.db_connection import get_db_connection
from flask import current_app

def get_all_students():
    """获取所有学生信息"""
    try:
        with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM students")
            return cursor.fetchall()
    except Exception as e:
        current_app.logger.error(f"Database error when getting all students: {str(e)}")
        return None

def get_student_by_id(student_id):
    """根据学生 ID 获取学生信息和成绩"""
    try:
        with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
            # 查询学生基本信息
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            
            if student:
                # 查询学生成绩
                cursor.execute("SELECT * FROM scores WHERE student_id = %s", (student_id,))
                student['scores'] = cursor.fetchall()
            
            return student
    except Exception as e:
        current_app.logger.error(f"Database error when getting student by ID: {str(e)}")
        return None

def create_student(student_data):
    """创建新学生"""
    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            insert_query = """
                INSERT INTO students (student_id, name, password)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (
                student_data['student_id'],
                student_data['name'],
                student_data['password']
            ))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        current_app.logger.error(f"Database error when creating student: {str(e)}")
        return None

def update_student(student_id, student_data):
    """更新学生信息"""
    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            update_query = """
                UPDATE students
                SET name = %s, password = %s
                WHERE student_id = %s
            """
            cursor.execute(update_query, (
                student_data['name'],
                student_data['password'],
                student_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        current_app.logger.error(f"Database error when updating student: {str(e)}")
        return False

def delete_student(student_id):
    """删除学生信息"""
    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        current_app.logger.error(f"Database error when deleting student: {str(e)}")
        return False
