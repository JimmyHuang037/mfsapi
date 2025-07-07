from flask import Blueprint, jsonify, request, current_app
import mysql.connector
from mysql.connector import Error

login_bp = Blueprint('login', __name__)

# 登录接口
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        student_id = data.get('username')
        password = data.get('password')

        if not student_id or not password:
            return jsonify({'error': 'Username and password required'}), 400

        conn = current_app.config['get_connection']()
        if not conn:
            return jsonify({'error': 'Database connection error'}), 500
            
        cursor = conn.cursor(dictionary=True)
        
        # 添加错误处理
        try:
            cursor.execute("""
                SELECT student_id, name FROM students 
                WHERE student_id = %s AND password = %s
            """, (student_id, password))
            
            student = cursor.fetchone()
            
            if not student:
                return jsonify({'error': 'Invalid credentials'}), 401
                
        except Exception as e:
            current_app.logger.error(f"Database error: {str(e)}")
            return jsonify({'error': 'Database operation failed'}), 500
        finally:
            cursor.close()
            conn.close()
            
        return jsonify(student)
        
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500