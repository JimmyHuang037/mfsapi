from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row  # 使结果可转换为字典
    return conn

# 查询所有或根据条件查询（原 GET）
@app.route('/api/students', methods=['GET'])
def get_students():
    student_id = request.args.get('id')
    name = request.args.get('name')
    limit = request.args.get('limit', default=100, type=int)

    query = "SELECT * FROM students"
    if student_id:
        query += f" WHERE id = {student_id}"
    if name:
        query += f" WHERE name = '{name}'"
    query += f" LIMIT {limit}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in results])

# 新增学生（POST）
@app.route('/students/<string:student_id>/scores', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    name = data.get('name')
    age = data.get('age')

    if not name or age is None:
        return jsonify({'error': 'Name and age are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': new_id, 'name': name, 'age': age}), 201

# 修改学生信息（PUT）
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    name = data.get('name')
    age = data.get('age')

    if not name and age is None:
        return jsonify({'error': 'No fields to update'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404

    if name:
        cursor.execute("UPDATE students SET name = ? WHERE id = ?", (name, student_id))
    if age is not None:
        cursor.execute("UPDATE students SET age = ? WHERE id = ?", (age, student_id))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Student updated successfully'})

# 删除学生（DELETE）
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)