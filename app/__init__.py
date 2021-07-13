import sys
from os import path

sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logs.flask_log import Logger
from settings.config import config_dict
from com.utils.constants import EXTRA_ENV_CONFIG


class FlaskApp(object):

    def __init__(self, flask_conf, log_name):
        # log 文件名：
        self.log_name = log_name

        # Flask App 创建：
        self.app = Flask(__name__)

        # Flask 加载配置：
        self.flask_conf = flask_conf

        # 初始化 SQLAlchemy：
        self.db = SQLAlchemy()

        # 初始化 Redis：
        self.redis_client = None

    def create_flask_app(self):
        """
        flask应用配置
        """

        # 默认配置（从配置子类中加载）
        self.app.config.from_object(config_dict[self.flask_conf])

        # 额外配置（从环境变量中加载）
        self.app.config.from_envvar(EXTRA_ENV_CONFIG, silent=True)

    def register_bp(self):
        """
        注册蓝图:
        """
        pass

    def register_extensions(self):
        """
        组件初始化
        """
        # Logging 初始化
        Logger().init_app(self.app, log_name=self.log_name)

        # SQLAlchemy组件初始化
        self.db.init_app(self.app)

    def create_app(self):
        """
        创建应用 和 组件初始化
        """
        # 创建flask应用
        self.create_flask_app()

        # 注册蓝图
        self.register_bp()

        # 组件初始化
        self.register_extensions()

    # app 启动工具：
    def run(self):
        self.app.run(
            host=self.app.config["HANDLER_ADDR"],
            port=self.app.config["HANDLER_PORT"],
            debug=self.app.config["DEBUG"],
            threaded=self.app.config["THREADED"]
        )
