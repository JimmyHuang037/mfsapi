from flask import Flask
from flask_cors import CORS
from config import Config
from app.models.student import StudentModel
from app.main.routes import main_bp
from app.api.students import students_bp
from app.api.login.routes import login_bp
from app.api.score.routes import score_bp

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
    app.config['DB_HOST'] = app.config['DB_HOST']
    app.config['DB_USER'] = app.config['DB_USER']
    app.config['DB_PASSWORD'] = app.config['DB_PASSWORD']
    app.config['DB_NAME'] = app.config['DB_NAME']
    app.config['get_connection'] = StudentModel.get_connection

def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(score_bp, url_prefix='/score')
