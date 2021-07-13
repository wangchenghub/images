
class DefaultConfig:
    """
    默认配置
    """
    # mysql配置:
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = "root"
    PASSWORD = "123456"
    HOST = "127.0.0.1"
    PORT = "3306"
    DATABASE = "image"
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT,
        DRIVER,
        USERNAME,
        PASSWORD,
        HOST,
        PORT,
        DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False                 # 是否打印底层执行的SQL

    # 设置是否传递异常 , 如果为True, 则flask运行中的错误会显示到网页中, 如果为False, 则会输出到文件中
    PROPAGATE_EXCEPTIONS = False


class Config(DefaultConfig):
    """
    server conf
    """
    # Server Config:
    DEBUG = True  # 调试模式
    THREADED = True  # 多线程启动
    HANDLER_PORT = "8088"  # 监听端口
    HANDLER_ADDR = "0.0.0.0"  # 监听地址


config_dict = {
    "Default": DefaultConfig,
    "UserConfig": Config,
}
