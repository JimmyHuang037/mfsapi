import os

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Newuser1')
    DB_NAME = os.getenv('DB_NAME', 'student_db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
