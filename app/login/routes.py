from flask import Blueprint, jsonify, request, current_app
from app.services.auth_service import authenticate_user

login_bp = Blueprint('login', __name__)

def validate_request_data(data):
    """
    验证请求数据是否有效
    :param data: 请求的 JSON 数据
    :return: 若数据无效返回错误响应和状态码，有效则返回 None
    """
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    if not all(data.get(key) for key in ('student_id', 'password')):
        return jsonify({'error': 'student_id and password required'}), 400
    
    return None

# 登录接口
@login_bp.route('/login', methods=['POST'])
def login():
    print("收到登录请求:", request.json)
    try:
        data = request.get_json()
        if error := validate_request_data(data):
            return error

        student_id = data.get('student_id')
        password = data.get('password')

        if not (student := authenticate_user(student_id, password)):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

        return jsonify({'success': True, 'student': student})
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

    # 移除重复的示例代码部分
    return jsonify(success=False)
