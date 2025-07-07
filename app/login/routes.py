from flask import Blueprint, jsonify, request, current_app
from app.utility.db_connection import get_db_connection

login_bp = Blueprint('login', __name__)

def validate_request_data(data):
    """
    验证请求数据是否有效
    :param data: 请求的 JSON 数据
    :return: 若数据无效返回错误响应和状态码，有效则返回 None
    """
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    if not all(data.get(key) for key in ('username', 'password')):
        return jsonify({'error': 'Username and password required'}), 400
    
    return None

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
                SELECT student_id, name FROM students 
                WHERE student_id = %s AND password = %s
            """, (student_id, password))
            return cursor.fetchone()
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        return None

# 登录接口
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        if error := validate_request_data(request.get_json()):
            return error
        if not (student := authenticate_user(*request.get_json().values())):
            return jsonify({'error': 'Invalid credentials'}), 401
        return jsonify(student)
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500