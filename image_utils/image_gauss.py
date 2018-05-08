# -*- coding: utf-8 -*-
"""

image_gauss
~~~~~~~~~~~

introduction
使用此模块改变原图片的尺寸，主要是实现横版和竖版的转换，图片从横版变竖版需要上下拼接填充高斯模糊的图片，竖版变横版则需要左右拼接。

Usage
=====
>>> from image_utils import ImageConverter
>>> image = ImageConverter().generate_image(image_path="/path/to/origin_image.jpg", des_ratio=1.6)
>>> image.save("/path/to/result.jpg")

"""

from PIL import Image, ImageFilter


class GaussianBlur(ImageFilter.Filter):
    """
    对图片进行高斯模糊
    """
    def __init__(self, radius=2, bounds=None):
        """

        :param radius: 模糊半径
        :param bounds: 模糊边界

        """
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        """ 填充模糊色

        :param image: 模糊前的图片image对象
        :return: 模糊后的图片Image对象

        """
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


class ImageConverter(object):

    @classmethod
    def generate_slide_image(cls, origin_image, slide_image, slide):
        """ 生成边缘图片

        :param origin_image: 原始图片
        :param slide_image: 需要填充颜色的图片
        :param slide: 字符串。left： 左侧，right：右侧，top：顶部，bottom：底部
        :return: 边缘图片的Image对象

        """
        if slide == "left":
            for i in xrange(0, origin_image.height):
                color = origin_image.getpixel((0, i))
                colored_image = Image.new(mode="RGB", size=(slide_image.width, 1), color=color)
                slide_image.paste(colored_image, (0, i))
        elif slide == "right":
            for i in xrange(0, origin_image.height):
                color = origin_image.getpixel((origin_image.width-1, i))
                colored_image = Image.new(mode="RGB", size=(slide_image.width, 1), color=color)
                slide_image.paste(colored_image, (0, i))
        elif slide == "top":
            for i in xrange(0, origin_image.width):
                color = origin_image.getpixel((i, 0))
                colored_image = Image.new(mode="RGB", size=(1, slide_image.height), color=color)
                slide_image.paste(colored_image, (i, 0))
        elif slide == "bottom":
            for i in xrange(0, origin_image.width):
                color = origin_image.getpixel((i, origin_image.height-1))
                colored_image = Image.new(mode="RGB", size=(1, slide_image.height), color=color)
                slide_image.paste(colored_image, (i, 0))
        slide_image.filter(GaussianBlur(radius=15))
        return slide_image

    @classmethod
    def merge_image(cls, origin_image, slide_images, direct):
        """ 将3张图片进行拼接

        :param origin_image: 原始图片，拼接在中间
        :param slide_images: 边缘图片，元组类型，如果图片是上下拼接，第一个值表示最上方的图片，如果是左右拼接，第一个值表示最左边的图片
        :param direct: 拼接方向，字符串类型，horizon表示左右拼接，其他值则认为是上下拼接
        :return: 返回拼接成功的图片的Image对象

        """
        if direct == "horizon":
            width = origin_image.width + sum([i.width for i in slide_images])
            image = Image.new(mode="RGB", size=(width, origin_image.height))
            image.paste(slide_images[0], (0, 0))
            image.paste(origin_image, (slide_images[0].width, 0))
            image.paste(slide_images[1], (slide_images[0].width + origin_image.width, 0))
        else:
            height = origin_image.height + sum([i.height for i in slide_images])
            image = Image.new(mode="RGB", size=(origin_image.width, height))
            image.paste(slide_images[0], (0, 0))
            image.paste(origin_image, (0, slide_images[0].height))
            image.paste(slide_images[1], (0, slide_images[0].height + origin_image.height))
        return image

    def generate_image(self, image_path, des_ratio):
        """ 生成带有高斯模糊的拓补图片

        :param image_path: 图片地址
        :param des_ratio: 图片调整之后的宽高比
        :return: 生成的图片的Image对象

        """
        image = Image.open(image_path)
        width, height = image.width, image.height
        if (width/height < 1 and des_ratio < 1) or (width/height > 1 and des_ratio > 1) or (width/height == des_ratio):
            return False
        if des_ratio > 1:
            w = des_ratio * height - width
            h = height
            slide_image = Image.new(mode="RGB", size=(int(w/2), h), color=(255, 255, 255))
            left_image = self.generate_slide_image(origin_image=image, slide_image=slide_image, slide="left")
            right_image = self.generate_slide_image(origin_image=image, slide_image=slide_image, slide="right")
            new_image = self.merge_image(image, (left_image, right_image), "horizon")
            return new_image
        else:
            w = width
            h = width / des_ratio - height
            slide_image = Image.new(mode="RGB", size=(w, int(h/2)), color=(255, 255, 255))
            top_image = self.generate_slide_image(origin_image=image, slide_image=slide_image, slide="top")
            bottom_image = self.generate_slide_image(origin_image=image, slide_image=slide_image, slide="bottom")
            new_image = self.merge_image(image, (top_image, bottom_image), "vertical")
            return new_image


if __name__ == '__main__':
    path = "/path/to/8eb2a9ec8a136327975f7b659d8fa0ec09fac7a0.jpg"
    d_image = ImageConverter().generate_image(path, 1.2)
    d_image.save("/path/to/result.jpg")
    path = "/path/to/m1.png"
    d_image = ImageConverter().generate_image(path, 0.8)
    d_image.save("/path/to/result2.jpg")
