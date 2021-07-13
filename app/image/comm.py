import math

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops


def add_mark(mark, kwargs):
    """
    添加水印，然后保存图片
    """
    with Image.open(kwargs.get("image")) as im:
        image = mark(im)
        if image:
            image = image.convert('RGB')
            return image


def set_opacity(im, opacity):
    """
    设置水印透明度
    """
    assert 0 <= opacity <= 1

    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def crop_image(im):
    """裁剪图片边缘空白"""
    bg = Image.new(mode='RGBA', size=im.size)
    diff = ImageChops.difference(im, bg)
    del bg
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im


def gen_mark(kwargs):
    """
    生成mark图片，返回添加水印的函数
    """
    # 字体宽度
    width = len(kwargs.get("mark")) * kwargs.get("size")

    # 创建水印图片(宽度、高度)
    mark = Image.new(mode='RGBA', size=(width, kwargs.get("size")))

    # 生成文字
    draw_table = ImageDraw.Draw(im=mark)
    draw_table.text(xy=(0, 0),
                    text=kwargs.get("mark"),
                    fill=kwargs.get("color"),
                    font=ImageFont.truetype(kwargs.get("font"),
                                            size=kwargs.get("size")))
    del draw_table

    # 裁剪空白
    mark = crop_image(mark)

    # 透明度
    set_opacity(mark, kwargs.get("opacity"))

    def mark_im(im):
        """ 在im图片上添加水印 im为打开的原图"""

        # 计算斜边长度
        c = int(math.sqrt(im.size[0] * im.size[0] + im.size[1] * im.size[1]))

        # 以斜边长度为宽高创建大图（旋转后大图才足以覆盖原图）
        mark2 = Image.new(mode='RGBA', size=(c, c))

        # 在大图上生成水印文字，此处mark为上面生成的水印图片
        y, idx = 0, 0
        while y < c:
            # 制造x坐标错位
            x = -int((mark.size[0] + kwargs.get("space")) * 0.5 * idx)
            idx = (idx + 1) % 2

            while x < c:
                # 在该位置粘贴mark水印图片
                mark2.paste(mark, (x, y))
                x = x + mark.size[0] + kwargs.get("space")
            y = y + mark.size[1] + kwargs.get("space")

        # 将大图旋转一定角度
        mark2 = mark2.rotate(kwargs.get("angle"))

        # 在原图上添加大图水印
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        im.paste(mark2,  # 大图
                 (int((im.size[0] - c) / 2), int((im.size[1] - c) / 2)),  # 坐标
                 mask=mark2.split()[3])
        del mark2
        return im

    return mark_im


def create_img(kwargs):
    mark = gen_mark(kwargs)
    return add_mark(mark, kwargs)
