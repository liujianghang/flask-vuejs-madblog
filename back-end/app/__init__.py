from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# plugin init
# Flask-SQLAlchemy plugin
db = SQLAlchemy()
# Flask-Migrate plugin
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # enable CORS
    CORS(app)
    # enable db
    db.init_app(app)
    # enable migrate
    migrate.init_app(app,db)

    # 注册 blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/', methods=['GET'])
    def ping():
        '''前端Vue.js用来测试与后端Flask API的连通性'''
        return jsonify('Pong!')

    return app


# 在最后处导入数据库表格模型
from app import models