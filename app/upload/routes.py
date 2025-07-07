from flask import Blueprint, jsonify, request, current_app
import os
import pandas as pd
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/import', methods=['POST'])
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
        filepath = os.path.join(current_app.config['DB_NAME'], UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f"📄 文件已保存: {filepath}")

        # 读取 Excel
        df = pd.read_excel(filepath)
        print("📊 Excel 读取成功:", df.head())

        # 获取数据库连接
        conn = current_app.config['get_connection']()
        cursor = conn.cursor()
        
        # 批量插入学生数据
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