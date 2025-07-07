from flask import Blueprint, jsonify, request
from app.services.student_service import (
    get_all_students, get_student_by_id, create_student,
    update_student, delete_student
)

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def list_students():
    """获取所有学生信息"""
    students = get_all_students()
    if students is None:
        return jsonify({'error': 'Failed to fetch students'}), 500
    return jsonify(students)

@students_bp.route('/<string:student_id>', methods=['GET'])
def get_student(student_id):
    """根据学生 ID 获取学生信息"""
    student = get_student_by_id(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student)

@students_bp.route('/', methods=['POST'])
def add_student():
    """创建新学生"""
    data = request.get_json()
    if not data or not all(key in data for key in ['student_id', 'name', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    student_id = create_student(data)
    if student_id is None:
        return jsonify({'error': 'Failed to create student'}), 500
    return jsonify({'message': 'Student created successfully', 'student_id': student_id}), 201

@students_bp.route('/<string:student_id>', methods=['PUT'])
def edit_student(student_id):
    """更新学生信息"""
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    if not update_student(student_id, data):
        return jsonify({'error': 'Student not found or update failed'}), 404
    return jsonify({'message': 'Student updated successfully'}), 200

@students_bp.route('/<string:student_id>', methods=['DELETE'])
def remove_student(student_id):
    """删除学生信息"""
    if not delete_student(student_id):
        return jsonify({'error': 'Student not found or delete failed'}), 404
    return jsonify({'message': 'Student deleted successfully'}), 200