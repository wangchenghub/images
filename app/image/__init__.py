from flask import Blueprint
from flask_restful import Api

from app.image.api.api import RotateResource, WatermarkResource, ThumbnailResource, CropResource, FormatResource

# 创建蓝图对象:
image_bp = Blueprint('image', __name__)

# 创建Api对象:
image_api = Api(image_bp)

# 设置json包装格式:
# image_api.representation('application/json')(output_json)

prefix = "/api/v1"

# image server Interface:
image_api.add_resource(RotateResource, f"{prefix}/rotate/<int:angle>")
image_api.add_resource(WatermarkResource, f"{prefix}/watermark")
image_api.add_resource(ThumbnailResource, f"{prefix}/thumbnail")
image_api.add_resource(CropResource, f"{prefix}/crop")
image_api.add_resource(FormatResource, f"{prefix}/format/<str:fm>")
