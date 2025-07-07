from flask import Blueprint, jsonify, request, current_app
import mysql.connector
from mysql.connector import Error

students_bp = Blueprint('students', __name__)

# 获取所有学生
@students_bp.route('/', methods=['GET'])
def get_students():
    conn = current_app.config['get_connection']()
    if not conn:
        return jsonify({'error': 'Database connection error'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)