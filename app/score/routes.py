from .routes import score_bp
from flask import Blueprint, jsonify, request, current_app
import mysql.connector
from mysql.connector import Error

score_bp = Blueprint('score', __name__)

# 注册蓝图路由
def init_score_routes(app):
    app.register_blueprint(score_bp, url_prefix='/scores')
    
# 获取单个学生成绩
@score_bp.route('/<string:student_id>', methods=['GET'])
def get_scores(student_id):
    conn = current_app.config['get_connection']()
    if not conn:
        return jsonify({'error': 'Database connection error'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM scores WHERE student_id = %s", (student_id,))
    scores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(scores)

# 添加学生成绩
def add_score(student_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        subject = data.get('subject')
        score_type = data.get('type')
        score_value = data.get('score')

        if not subject or not score_type or score_value is None:
            return jsonify({'error': 'Subject, type and score are required'}), 400

        conn = current_app.config['get_connection']()
        if not conn:
            return jsonify({'error': 'Database connection error'}), 500

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scores (student_id, subject, type, score) VALUES (%s, %s, %s, %s)",
            (student_id, subject, score_type, score_value)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'id': new_id,
            'student_id': student_id,
            'subject': subject,
            'type': score_type,
            'score': score_value
        }), 201

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# 修改学生成绩
def update_score(student_id, score_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        subject = data.get('subject')
        score_type = data.get('type')
        score_value = data.get('score')

        if subject is None and score_type is None and score_value is None:
            return jsonify({'error': 'No fields to update'}), 400

        conn = current_app.config['get_connection']()
        if not conn:
            return jsonify({'error': 'Database connection error'}), 500

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
            return jsonify({'error': 'Score record not found'}), 404

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

        return jsonify({'message': 'Score updated successfully'})

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# 删除学生成绩
def delete_score(student_id, score_id):
    try:
        conn = current_app.config['get_connection']()
        if not conn:
            return jsonify({'error': 'Database connection error'}), 500

        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM scores WHERE student_id = %s AND id = %s",
            (student_id, score_id)
        )
        record = cursor.fetchone()
        if not record:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Score record not found'}), 404

        cursor.execute(
            "DELETE FROM scores WHERE student_id = %s AND id = %s",
            (student_id, score_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Score deleted successfully'})

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500