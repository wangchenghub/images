from app import FlaskApp


class ImageService(FlaskApp):
    def __init__(self, flask_conf):
        super().__init__(flask_conf=flask_conf, log_name="image.log")

    def register_bp(self):
        """
        注册蓝图:
        """
        from app.image import image_bp
        self.app.register_blueprint(image_bp)


service = ImageService('UserConfig')


def init():
    service.create_app()
    app = service.app
    return app
