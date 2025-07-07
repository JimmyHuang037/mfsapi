from flask import Flask
from factory import create_app

# 创建Flask应用
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)