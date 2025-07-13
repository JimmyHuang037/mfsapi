from flask import Flask
from flask_cors import CORS
from config import Config

cors = CORS()

def create_app(config_class=Config):
    from app.utility.db_connection import get_db_connection
    from app.students.routes import students_bp
    from app.score.routes import score_bp
    from app.login.routes import login_bp
    from app.upload.routes import upload_bp

    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    cors.init_app(app)

    # 注册蓝图
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(score_bp, url_prefix='/api/scores')
    app.register_blueprint(login_bp, url_prefix='/api/login')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')

    # 存储获取数据库连接的函数
    app.config['get_connection'] = get_db_connection

    return app