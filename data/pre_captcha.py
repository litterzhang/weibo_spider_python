#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'对验证码进行预处理'

__author__='litterzhang'

import os
from PIL import Image, ImageEnhance, ImageFilter

# 处理图片以便后续的0-1二值化
def Handle_Image(im):
    im = im.convert('RGB')

    for j in range(im.size[1]):
        for i in range(im.size[0]):
            if i == 0 or i == (im.size[0] - 1):  # 将图片的第一行和最后一行设为白色。
                im.putpixel([i, j], (255, 255, 255))
            if j == 0 or j == (im.size[1] - 1):  # 将图片的第一列和最后一列设为白色。
                im.putpixel([i, j], (255, 255, 255))

            color = im.getpixel((i, j))
            if sum(color)<450:
                im.putpixel([i, j], (0, 0, 0))
            else:
                im.putpixel([i, j], (255, 255, 255))

    im = im.convert('1')

    im = Clear_Point(im)  # 清除周围8个像素都是白色的孤立噪点
    im = Clear_Point_Twice(im)  # 清除两个孤立的噪点：周围8个像素中有7个是白色，而唯一的黑色像素对应的他的邻域（他周围的8个像素）中唯一的黑色像素是自身。

    im = Clear_line(im)
    im = Clear_Point(im)
    im = Clear_Point_Twice(im)
    return im

# 初步清除干扰线
def Clear_line(im):
    Image_Value = Caculate_X(im)
    for i in range(1, len(Image_Value)-1):
        if Image_Value[i]==1:
            for j in range(1, im.size[1] - 1):
                if im.getpixel((i, j))==0:
                    im.putpixel([i, j], 255)
        if Image_Value[i]==2:
            for j in range(1, im.size[1] - 1):
                if im.getpixel((i, j))==0 and im.getpixel((i, j+1))==0:
                    im.putpixel([i, j], 255)
                    im.putpixel([i, j+1], 255)
    return im

# 清除单个孤立点
def Clear_Point(im):
    for j in range(1, (im.size[1] - 1)):
        for i in range(1, (im.size[0] - 1)):
            if im.getpixel((i, j)) == 0 and im.getpixel(((i - 1), (j - 1))) == 255 and im.getpixel(
                    (i, (j - 1))) == 255 and im.getpixel(((i + 1), (j - 1))) == 255 and im.getpixel(
                    ((i - 1), j)) == 255 and im.getpixel(((i + 1), j)) == 255 and im.getpixel(
                    ((i - 1), (j + 1))) == 255 and im.getpixel((i, (j + 1))) == 255 and im.getpixel(
                    ((i + 1), (j + 1))) == 255:
                im.putpixel([i, j], 255)
    return im

# TODO 检查一下符号
def Clear_Point_Twice(im):
    for j in range(1, (im.size[1] - 1)):
        for i in range(1, (im.size[0] - 1)):
            if im.getpixel((i, j)) == 0 and (im.getpixel(((i - 1), (j - 1))) + im.getpixel((i, (j - 1))) + im.getpixel(
                    ((i + 1), (j - 1))) + im.getpixel(((i - 1), j)) + im.getpixel(((i + 1), j)) + im.getpixel(
                    ((i - 1), (j + 1))) + im.getpixel((i, (j + 1))) + im.getpixel(((i + 1), (j + 1)))) == 255 * 7:
                if im.getpixel(((i + 1), j)) == 0:  # 因为扫描的顺序是从上到下，从左到右，噪点只能是在自身像素的后面和下面，也就是只有4个可能性而已，而不是8个，可以减少一半的代码。
                    m = i + 1
                    n = j
                    if (im.getpixel(((m - 1), (n - 1))) + im.getpixel((m, (n - 1))) + im.getpixel(
                            ((m + 1), (n - 1))) + im.getpixel(((m - 1), n)) + im.getpixel(((m + 1), n)) + im.getpixel(
                            ((m - 1), (n + 1))) + im.getpixel((m, (n + 1))) + im.getpixel(
                            ((m + 1), (n + 1)))) == 255 * 7:
                        im.putpixel([i, j], 255)
                        im.putpixel([m, n], 255)
                elif im.getpixel(((i - 1), (j + 1))) == 0:
                    m = i - 1
                    n = j + 1
                    if (im.getpixel(((m - 1), (n - 1))) + im.getpixel((m, (n - 1))) + im.getpixel(
                            ((m + 1), (n - 1))) + im.getpixel(((m - 1), n)) + im.getpixel(((m + 1), n)) + im.getpixel(
                            ((m - 1), (n + 1))) + im.getpixel((m, (n + 1))) + im.getpixel(
                            ((m + 1), (n + 1)))) == 255 * 7:
                        im.putpixel([i, j], 255)
                        im.putpixel([m, n], 255)
                elif im.getpixel((i, (j + 1))) == 0:
                    m = i
                    n = j + 1
                    if (im.getpixel(((m - 1), (n - 1))) + im.getpixel((m, (n - 1))) + im.getpixel(
                            ((m + 1), (n - 1))) + im.getpixel(((m - 1), n)) + im.getpixel(((m + 1), n)) + im.getpixel(
                            ((m - 1), (n + 1))) + im.getpixel((m, (n + 1))) + im.getpixel(
                            ((m + 1), (n + 1)))) == 255 * 7:
                        im.putpixel([i, j], 255)
                        im.putpixel([m, n], 255)
                elif im.getpixel(((i + 1), (j + 1))) == 0:
                    m = i + 1
                    n = j + 1
                    if (im.getpixel(((m - 1), (n - 1))) + im.getpixel((m, (n - 1))) + im.getpixel(
                            ((m + 1), (n - 1))) + im.getpixel(((m - 1), n)) + im.getpixel(((m + 1), n)) + im.getpixel(
                            ((m - 1), (n + 1))) + im.getpixel((m, (n + 1))) + im.getpixel(
                            ((m + 1), (n + 1)))) == 255 * 7:
                        im.putpixel([i, j], 255)
                        im.putpixel([m, n], 255)
    return im

# 依据图片像素颜色计算X轴投影
def Caculate_X(im):
    Image_Value = []
    for i in range(im.size[0]):
        Y_pixel = 0
        for j in range(im.size[1]):
            if im.getpixel((i, j)) == 0:
                temp_value = 1
            else:
                temp_value = 0
            Y_pixel = Y_pixel + temp_value
        Image_Value.append(Y_pixel)
    return Image_Value

# x轴投影
def Get_X(Image_Value):
    X_Value = []
    for i in range(len(Image_Value[0])):  # 51
        Y_pixel = 0
        for j in range(len(Image_Value)):
            Y_pixel = Y_pixel + Image_Value[j][i]
        X_Value.append(Y_pixel)
    return X_Value  # 51

# Y轴投影
def Get_Y(Image_Value):
    Y_Value = []
    for j in range(len(Image_Value)):  # 16
        X_pixel = 0
        for i in range(len(Image_Value[0])):
            X_pixel = X_pixel + Image_Value[j][i]
        Y_Value.append(X_pixel)
    return Y_Value

# 处理图片
def handle(loaddirpath, savedirpath):
    for filename in os.listdir(loaddirpath):
        filepath = os.path.join(loaddirpath, filename)

        im = Image.open(filepath)
        im = Handle_Image(im)

        im.save(os.path.join(savedirpath, 'pre_%s' % filename))
        # break

if __name__=='__main__':
    handle(os.path.join(os.path.dirname(__file__), 'img'), \
        os.path.join(os.path.dirname(__file__), 'pre_img'))