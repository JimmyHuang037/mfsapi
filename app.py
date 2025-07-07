from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
CORS(app)  # 允许所有来源

# 数据库配置
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Newuser1')
DB_NAME = os.getenv('DB_NAME', 'student_db')

# 创建数据库连接
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# 初始化数据库
def init_db():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        with open('migrations/create_tables.sql', 'r') as f:
            sql_file = f.read()
        sql_commands = sql_file.split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
        conn.commit()
        cursor.close()
        conn.close()

# 获取所有学生
@app.route('/students', methods=['GET'])
def get_students():
    conn = create_connection()
    if not conn:
        return jsonify({'error': 'Database connection error'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

# 获取单个学生成绩
@app.route('/students/<string:student_id>/scores', methods=['GET'])
def get_scores(student_id):
    conn = create_connection()
    if not conn:
        return jsonify({'error': 'Database connection error'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM scores WHERE student_id = %s", (student_id,))
    scores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(scores)

# 添加学生成绩
@app.route('/students/<string:student_id>/scores', methods=['POST'])
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

        conn = create_connection()
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
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# 修改学生成绩
@app.route('/students/<string:student_id>/scores/<int:score_id>', methods=['PUT'])
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

        conn = create_connection()
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
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# 删除学生成绩
@app.route('/students/<string:student_id>/scores/<int:score_id>', methods=['DELETE'])
def delete_score(student_id, score_id):
    try:
        conn = create_connection()
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
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# 登录接口
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        student_id = data.get('username')
        password = data.get('password')

        if not student_id or not password:
            return jsonify({'error': 'Username and password required'}), 400

        conn = create_connection()
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
                
            cursor.execute("""
                SELECT subject, type, score FROM scores 
                WHERE student_id = %s
            """, (student_id,))
            
            scores = cursor.fetchall()
            student['scores'] = scores
            
        except Exception as e:
            app.logger.error(f"Database error: {str(e)}")
            return jsonify({'error': 'Database operation failed'}), 500
        finally:
            cursor.close()
            conn.close()
            
        return jsonify(student)
        
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


    if student:
        return jsonify(student)
    else:
        return jsonify({'error': 'Invalid credentials'}), 401



from flask import Flask, request, jsonify
import os
import pandas as pd
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
# 配置
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}
app.config['DB_CONFIG'] = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Newuser1',
    'database': 'student_db'
}
# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_db_connection():
    return mysql.connector.connect(**app.config['DB_CONFIG'])


@app.route('/students', methods=['GET'])
def get_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/import', methods=['POST'])
def import_excel():
    try:
        print("📥 收到上传请求")
        if 'file' not in request.files:
            print("❌ 没有 file 字段")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            print("❌ 文件名为空")
            return jsonify({'error': 'No selected file'}), 400

        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"📄 文件已保存: {filepath}")

        # 读取 Excel
        import pandas as pd
        df = pd.read_excel(filepath, engine='openpyxl')
        print("📊 Excel 读取成功:", df.head())

        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        for index, row in df.iterrows():
            columns = ['student_id', 'name', 'password']  # 不要包含 id
            values = [row[col] for col in columns]
            placeholders = ', '.join(['%s'] * len(columns))
            sql = f"INSERT INTO students ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(values))
        conn.commit()
        cursor.close()
        conn.close()

        # 删除临时文件
        os.remove(filepath)

        return jsonify({'status': 'success', 'message': f'成功导入 {len(df)} 条记录'}), 200

    except Exception as e:
        print("❌ 错误信息:", str(e))  # 最重要：打印报错内容！
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
