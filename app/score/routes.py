from flask import Blueprint, jsonify, request, current_app
from app.services.score_service import get_scores, add_score, update_score, delete_score

score_bp = Blueprint('score', __name__)

def init_score_routes(app):
    app.register_blueprint(score_bp, url_prefix='/scores')

# 获取单个学生成绩
@score_bp.route('/<string:student_id>', methods=['GET'])
def get_scores_route(student_id):
    scores = get_scores(student_id)
    if scores is None:
        return jsonify({'error': 'Failed to fetch scores'}), 500
    return jsonify(scores)

# 添加学生成绩
@score_bp.route('/<string:student_id>/scores', methods=['POST'])
def add_score_route(student_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    subject = data.get('subject')
    score_type = data.get('type')
    score_value = data.get('score')

    if not subject or not score_type or score_value is None:
        return jsonify({'error': 'Subject, type and score are required'}), 400

    new_id = add_score(student_id, subject, score_type, score_value)
    if new_id is None:
        return jsonify({'error': 'Failed to add score'}), 500

    return jsonify({
        'id': new_id,
        'student_id': student_id,
        'subject': subject,
        'type': score_type,
        'score': score_value
    }), 201

# 修改学生成绩
@score_bp.route('/<string:student_id>/scores/<int:score_id>', methods=['PUT'])
def update_score_route(student_id, score_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    subject = data.get('subject')
    score_type = data.get('type')
    score_value = data.get('score')

    if subject is None and score_type is None and score_value is None:
        return jsonify({'error': 'No fields to update'}), 400

    if not update_score(student_id, score_id, subject, score_type, score_value):
        return jsonify({'error': 'Score record not found or update failed'}), 404

    return jsonify({'message': 'Score updated successfully'})

# 删除学生成绩
@score_bp.route('/<string:student_id>/scores/<int:score_id>', methods=['DELETE'])
def delete_score_route(student_id, score_id):
    if not delete_score(student_id, score_id):
        return jsonify({'error': 'Score record not found or delete failed'}), 404

    return jsonify({'message': 'Score deleted successfully'})