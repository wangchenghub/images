import io
import base64

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import flask
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from app.image.comm import create_img


class CommResource(Resource):

    @staticmethod
    def get_args_img():
        """
        获取参数： 只获取 imgFile
        """
        parser = RequestParser()
        parser.add_argument("imgFile", required=True, type=FileStorage, location='files', help="imgFile is wrong.")
        args = parser.parse_args()
        return args.get("imgFile")

    @staticmethod
    def get_byte_image(img, fm="jpg"):
        """
        图片编码
        """
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=fm)
        encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        return encoded_img

    @staticmethod
    def watermark_format(**kwargs):
        font = kwargs.get("font", )
        size = kwargs.get("size", )
        image  = kwargs.get("image", )
        x = kwargs.get("x")
        y = kwargs.get("y")
        words = kwargs.get("words")
        colour = kwargs.get("colour")

        # 创建字体对象：
        obj_font = ImageFont.truetype(font=font, size=size)

        # 创建画板对象：
        obj_draw = ImageDraw.Draw(image)

        # 渲染水印：text(坐标， 文自内容， 文字颜色, 文字对象)
        obj_draw.text(xy=(x, y), text=words, fill=colour, font=obj_font)

        return image


class RotateResource(CommResource):
    """
    图片旋转：
    """
    @staticmethod
    def post(angle):
        # 获取图片：
        imgFile = RotateResource.get_args_img()

        with Image.open(imgFile.stream) as img:
            img.rotate(angle=angle)
            image = RotateResource.get_byte_image(img, imgFile.filename.split(".")[-1])
            response = {'Status': 'Success', 'message': "", 'ImageBytes': image}
            return flask.jsonify(response)


class WatermarkResource(CommResource):
    """
    图片水印：
    """
    @staticmethod
    def post():
        # 获取图片：
        imgFile = WatermarkResource.get_args_img()

        # 获取参数：
        parser = RequestParser()
        parser.add_argument("font", required=True, type=str, location='from', help="Watermark font")
        parser.add_argument("mark", required=True, type=str, location='from', help="Watermark content")
        parser.add_argument("color", required=True, type=str, location='from', help="Watermark text color")
        parser.add_argument("space", required=True, type=int, location='from', help="Spacing between watermarks")
        parser.add_argument("angle", required=True, type=int, location='from', help="Rotation angle of watermark")
        parser.add_argument("size", required=True, type=int, location='from', help="The font size of the text")
        parser.add_argument("opacity", required=True, type=int, location='from', help="Opacity of watermark")
        parser.add_argument("quality", required=True, type=int, location='from', help="Output image quality")
        args = parser.parse_args()

        kwargs = {
            "font": args.get("font", "Medium.ttf"),        # 水印字体
            "image": imgFile,                              # 图像文件路径或目录
            "mark": args.get("mark", "内部文件,请勿外传"),    # 水印内容
            "color": args.get("color", "#A4A4A4"),         # 文本颜色 例如：“#000000”，默认为#8B1B
            "space": args.get("space", 500),               # 水印之间的间距，默认值为100
            "angle": args.get("angle", 30),                # 旋转水印的角度，默认为30
            "size": args.get("size", 300),                 # 文本的字体大小，默认为50
            "opacity": args.get("opacity", 0.15),          # 水印的不透明度，默认值为0.15
            "quality": args.get("quality", 90)             # 输出图像质量，默认为90
        }

        new_image = create_img(kwargs)
        image = RotateResource.get_byte_image(new_image, imgFile.filename.split(".")[-1])
        response = {'Status': 'Success', 'message': "", 'ImageBytes': image}
        return flask.jsonify(response)


class ThumbnailResource(CommResource):
    """
    图片缩放
    """
    @staticmethod
    def post():
        # 获取图片：
        imgFile = ThumbnailResource.get_args_img()

        # 获取参数：
        parser = RequestParser()
        parser.add_argument("length", required=True, type=int, location='json', help="Picture length")
        parser.add_argument("width", required=True, type=int, location='json', help="image width")
        args = parser.parse_args()

        with Image.open(imgFile.stream) as img:
            img.thumbnail((args.length, args.width))
            image = RotateResource.get_byte_image(img, imgFile.filename.split(".")[-1])
            response = {'Status': 'Success', 'message': "", 'ImageBytes': image}
            return flask.jsonify(response)


class CropResource(CommResource):
    """
    图片裁剪
    """
    @staticmethod
    def post():
        # 获取图片：
        imgFile = CropResource.get_args_img()

        # 获取参数：
        parser = RequestParser()
        parser.add_argument("X_coordinate", required=True, type=tuple, location='json', help="X coordinate")
        parser.add_argument("y_coordinate", required=True, type=tuple, location='json', help="y coordinate")
        args = parser.parse_args()

        with Image.open(imgFile.stream) as img:
            img.crop(args.X_coordinate, args.y_coordinate)
            image = CropResource.get_byte_image(img, imgFile.filename.split(".")[-1])
            response = {'Status': 'Success', 'message': "", 'ImageBytes': image}
            return flask.jsonify(response)


class FormatResource(CommResource):
    """
    图片格式：
    """
    @staticmethod
    def get(fm):
        # 获取图片：
        imgFile = RotateResource.get_args_img()

        with Image.open(imgFile.stream) as img:
            image = RotateResource.get_byte_image(img, fm)
            response = {'Status': 'Success', 'message': "", 'ImageBytes': image}
            return flask.jsonify(response)
