from app.utility.db_connection import get_db_connection

class StudentModel:
    @staticmethod
    def get_all_students():
        """获取所有学生信息"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            return students
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_scores_by_student_id(student_id):
        conn = StudentModel.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM scores WHERE student_id = %s", (student_id,))
        scores = cursor.fetchall()
        cursor.close()
        conn.close()
        return scores

    @staticmethod
    def add_score(student_id, subject, score_type, score_value):
        conn = StudentModel.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scores (student_id, subject, type, score) VALUES (%s, %s, %s, %s)",
            (student_id, subject, score_type, score_value)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {
            'id': new_id,
            'student_id': student_id,
            'subject': subject,
            'type': score_type,
            'score': score_value
        }

    @staticmethod
    def update_score(student_id, score_id, subject=None, score_type=None, score_value=None):
        conn = StudentModel.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        # 检查是否存在该成绩记录
        cursor.execute(
            "SELECT * FROM scores WHERE student_id = %s AND id = %s",
            (student_id, score_id)
        )
        record = cursor.fetchone()
        if not record:
            cursor.close()
            conn.close()
            return {'error': 'Score record not found'}, 404

        # 构建更新语句
        update_fields = []
        values = []
        if subject:
            update_fields.append("subject = %s")
            values.append(subject)
        if score_type:
            update_fields.append("type = %s")
            values.append(score_type)
        if score_value is not None:
            update_fields.append("score = %s")
            values.append(score_value)

        values.append(student_id)
        values.append(score_id)
        update_query = f"UPDATE scores SET {', '.join(update_fields)} WHERE student_id = %s AND id = %s"

        cursor.execute(update_query, tuple(values))
        conn.commit()
        cursor.close()
        conn.close()
        return {'message': 'Score updated successfully'}

    @staticmethod
    def delete_score(student_id, score_id):
        conn = StudentModel.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM scores WHERE student_id = %s AND id = %s",
            (student_id, score_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {'message': 'Score deleted successfully'}