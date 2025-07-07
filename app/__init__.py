from flask import Flask
from flask_cors import CORS
import os
from config import Config
from app.models.student import StudentModel

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
    # 配置数据库
    app.config['DB_HOST'] = app.config['DB_HOST']
    app.config['DB_USER'] = app.config['DB_USER']
    app.config['DB_PASSWORD'] = app.config['DB_PASSWORD']
    app.config['DB_NAME'] = app.config['DB_NAME']
    # 添加获取数据库连接的方法
    app.config['get_connection'] = StudentModel.get_connection

def register_blueprints(app):
    """注册蓝图"""
    from app.main.routes import main_bp
    from app.api.students import students_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(students_bp, url_prefix='/students')