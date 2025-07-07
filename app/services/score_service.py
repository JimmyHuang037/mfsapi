from app.utility.db_connection import get_db_connection
from flask import current_app

def get_scores(student_id):
    """
    获取单个学生成绩
    :param student_id: 学生 ID
    :return: 学生成绩列表，出错返回 None
    """
    try:
        with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM scores WHERE student_id = %s", (student_id,))
            return cursor.fetchall()
    except Exception as e:
        current_app.logger.error(f"Error getting scores for student {student_id}: {str(e)}")
        return None

def add_score(student_id, subject, score_type, score_value):
    """
    添加学生成绩
    :param student_id: 学生 ID
    :param subject: 科目
    :param score_type: 成绩类型
    :param score_value: 成绩值
    :return: 新成绩记录 ID，出错返回 None
    """
    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO scores (student_id, subject, type, score) VALUES (%s, %s, %s, %s)",
                (student_id, subject, score_type, score_value)
            )
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        current_app.logger.error(f"Error adding score for student {student_id}: {str(e)}")
        return None

def update_score(student_id, score_id, subject=None, score_type=None, score_value=None):
    """
    修改学生成绩
    :param student_id: 学生 ID
    :param score_id: 成绩记录 ID
    :param subject: 科目
    :param score_type: 成绩类型
    :param score_value: 成绩值
    :return: 修改成功返回 True，未找到记录或出错返回 False
    """
    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            # 检查是否存在该成绩记录
            cursor.execute(
                "SELECT * FROM scores WHERE student_id = %s AND id = %s",
                (student_id, score_id)
            )
            if not cursor.fetchone():
                return False

            # 构建更新语句
            update_fields = []
            values = []
            if subject is not None:
                update_fields.append("subject = %s")
                values.append(subject)
            if score_type is not None:
                update_fields.append("type = %s")
                values.append(score_type)
            if score_value is not None:
                update_fields.append("score = %s")
                values.append(score_value)

            if not update_fields:
                return False

            values.append(student_id)
            values.append(score_id)
            update_query = f"UPDATE scores SET {', '.join(update_fields)} WHERE student_id = %s AND id = %s"

            cursor.execute(update_query, tuple(values))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        current_app.logger.error(f"Error updating score {score_id} for student {student_id}: {str(e)}")
        return False

def delete_score(student_id, score_id):
    """
    删除学生成绩
    :param student_id: 学生 ID
    :param score_id: 成绩记录 ID
    :return: 删除成功返回 True，未找到记录或出错返回 False
    """
    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            # 检查是否存在该成绩记录
            cursor.execute(
                "SELECT * FROM scores WHERE student_id = %s AND id = %s",
                (student_id, score_id)
            )
            if not cursor.fetchone():
                return False

            cursor.execute(
                "DELETE FROM scores WHERE student_id = %s AND id = %s",
                (student_id, score_id)
            )
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting score {score_id} for student {student_id}: {str(e)}")
        return False
