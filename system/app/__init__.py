from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
# import sys
import os


db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yjh383838@lcoalhost:3306/synthetic_data'

    # 初始化 SQLAlchemy
    db.init_app(app)

    # 导入并注册蓝图
    from .routes.home import home_bp
    from .routes.survery import survey_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(survey_bp,url_prefix='/survey')

    return app
