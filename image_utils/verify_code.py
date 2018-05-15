# -*- coding: utf-8 -*-
"""

verify_code
~~~~~~~~~~~

introduction
使用该模块生成验证码

Usage
=====
>>> import io
>>> from image_utils import VerifyCodeGenerator
>>> font_path='/usr/share/fonts/windows-fonts/仿宋_GB2312'
>>> generator = VerifyCodeGenerator(font_path)
>>> img_obj, text = generator.gene_code()
>>> buf = io.StringIO()
>>> img_obj.save(buf, 'png')
>>> http_response_value = img_obj.getvalue()

"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class VerifyCodeGenerator(object):
    """
    生成验证码的工具类
    """
    def __init__(self,
                 font_path,
                 number=4,
                 size=(129, 53),
                 bg_color=(255, 255, 255),
                 font_color=(0, 0, 0),
                 line_color=(0, 0, 0),
                 draw_line=True):
        """ 生成验证码工具类

        :param font_path: 字体文件路径
        :param number: 验证码字符串长度
        :param size: 验证码大小，接收一个元组，(宽, 高)
        :param bg_color: 背景色
        :param font_color: 字体颜色
        :param line_color: 干扰线颜色
        :param draw_line: 是否绘制干扰线

        """
        self._font_path = font_path
        self._number = number
        self._size = size
        self._bg_color = bg_color
        self._font_color = font_color
        self._line_color = line_color
        self._draw_line = draw_line

    def _gene_text(self):
        """ 生成验证码字符串

        :return: 验证码的字符串

        """
        source = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Z', 'X', 'Y', 'a', 'b', 'c', 'd',
                  'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                  'y', 'z']
        return ''.join(random.sample(source, self._number))

    def _gene_line(self, draw, height):
        """ 绘制干扰线

        :param draw: 图片绘制对象
        :param height: 干扰线宽度
        :return: None

        """
        begin = (0, random.randint(0, height))
        end = (74, random.randint(0, height))
        draw.line([begin, end], fill=self._line_color, width=3)

    def gene_code(self, file_name=None):
        """ 生成验证码

        :param file_name: 验证码存储的文件地址，若不填则不保存
        :return: 存储验证码信息的元组（验证码Image对象, 验证码字符串）

        """
        width, height = self._size
        image = Image.new('RGBA', (width, height), self._bg_color)
        font = ImageFont.truetype(self._font_path, 40)
        draw = ImageDraw.Draw(image)
        text = self._gene_text()
        font_width, font_height = font.getsize(text)
        draw.text(
            ((width - font_width) / self._number, (height - font_height) / self._number),
            text,
            font=font,
            fill=self._font_color
        )
        if self._draw_line:
            self._gene_line(draw, height)
        image = image.transform((width + 30, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        aa = str(".png")
        if file_name:
            path = file_name + text + aa
            image.save(path)
        return image, text


if __name__ == '__main__':
    generator = VerifyCodeGenerator(font_path='/usr/share/fonts/windows-fonts/仿宋_GB2312')
    for i in xrange(20):
        print generator.gene_code("./code_image/")
