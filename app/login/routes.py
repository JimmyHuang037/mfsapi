from flask import Blueprint, jsonify, request, current_app
from app.services.auth_service import authenticate_user
from app.services.score_service import get_scores

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
        return jsonify({'error': 'username and password required'}), 400
    
    return None

@login_bp.route('/', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if error := validate_request_data(data):
            return error

        username = data.get('username')
        password = data.get('password')

        if not (student := authenticate_user(username, password)):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

        if 'name' not in student:
            current_app.logger.error(f"Student name missing for {username}")
            return jsonify({'error': 'Student data incomplete'}), 500

        scores = get_scores(username)
        
        return jsonify({
            "username": username,  # 改为username
            "name": student['name'],
            "scores": scores if scores else []
        })
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500