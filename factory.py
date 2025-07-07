from flask import Flask
from flask_cors import CORS
from config import Config
from app.students.routes import students_bp
from app.login.routes import login_bp
from app.score.routes import score_bp
from app.upload.routes import upload_bp
from app.utility.db_connection import get_db_connection

cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    initialize_extensions(app)
    # 注册蓝图
    register_blueprints(app)

    return app

def initialize_extensions(app):
    """初始化扩展"""
    cors.init_app(app)  # 初始化 CORS
    app.config['get_connection'] = get_db_connection

def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(score_bp, url_prefix='/score')
    app.register_blueprint(upload_bp, url_prefix='/upload')