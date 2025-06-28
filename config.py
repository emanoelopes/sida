import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    UPLOAD_FOLDER = 'uploads'
