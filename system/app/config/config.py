import os
class Config:
    """Base configuration."""
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yjh383838@localhost:3306/employee_info'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
