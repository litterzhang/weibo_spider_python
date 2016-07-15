#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'对验证码进行预处理'

__author__='litterzhang'

import os
from PIL import Image, ImageEnhance, ImageFilter

# 处理图片以便后续的0-1二值化
def Handle_Image(im):
    im = im.convert('L')

    for j in range(im.size[1]):
        for i in range(im.size[0]):
            #Gray = Change_Gray(im.getpixel((i, j)))  # 灰度化
            #im.putpixel([i, j], (Gray, Gray, Gray))
            if i == 0 or i == (im.size[0] - 1):  # 将图片的第一行和最后一行设为白色。
                im.putpixel([i, j], 255)
            if j == 0 or j == (im.size[1] - 1):  # 将图片的第一列和最后一列设为白色。
                im.putpixel([i, j], 255)
    enhancer = ImageEnhance.Contrast(im)  # 增加对比对
    im = enhancer.enhance(2)
    enhancer = ImageEnhance.Sharpness(im)  # 锐化
    im = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(im)  # 增加亮度
    im = enhancer.enhance(2)
    im = im.filter(ImageFilter.DETAIL) #滤镜效果

    im = im.convert("1")

    im = Clear_Point(im)  # 清除周围8个像素都是白色的孤立噪点
    im = Clear_Point_Twice(im)  # 清除两个孤立的噪点：周围8个像素中有7个是白色，而唯一的黑色像素对应的他的邻域（他周围的8个像素）中唯一的黑色像素是自身。
    im = Clear_Point_Third(im)  # 清除第三种噪点：左右都是3个（含）以上的空白列，自身相邻的3个列上的X值投影不大于3.

    im = Clear_line(im)
    im = Clear_Point(im)
    im = Clear_Point_Twice(im)
    im = Clear_Point_Third(im) 
    return im

# 改变灰度，查文献后发现据说按照下面的R，G，B数值的比例进行调整，图像的灰度最合适。
def Change_Gray(RGB_Value):
    Gray = int((RGB_Value[0] * 299 + RGB_Value[1] * 587 + RGB_Value[2] * 114) / 1000)
    return Gray

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

def Set_White_Y(im, List_Black):
    for j in range(im.size[1]):
        for i in range(List_Black[0], (List_Black[(len(List_Black) - 1)])):
            im.putpixel([i, j], 255)
    return im

# 清除第三种残余的孤立点
def Clear_Point_Third(im):
    Image_Value = Caculate_X(im)
    List01 = []
    List_Black = []
    List03 = []
    for i in range(len(Image_Value)):  # 从左到右扫描
        if Image_Value[i] == 0 and len(List_Black) == 0:  # X轴投影是0，说明是空白列，黑色列的列表是空值，说明当前列是黑色列的左侧
            List01.append(i)
        elif Image_Value[i] > 0:  # X周投影大于0的列，即扫描到了黑色列
            List_Black.append(i)
        elif Image_Value[i] == 0 and len(List_Black) > 0 and len(
                List_Black) <= 3:  # 黑色列的列表的长度大于0，不大于3个空白字符，现在的X轴投影为0，说明现在扫描到了孤立噪点所在的黑色列右侧的空白列
            List03.append(i)
            if len(List03) == 3:  # 空白列为3列
                im = Set_White_Y(im, List_Black)  # 逐次将多列设为全白
                List01 = []
                List_Black = []
                List03 = []
        elif Image_Value[i] == 0 and len(List_Black) > 3:  # 当前是空白列，黑色列的数量大于3，说明扫描到了数字所在部分（不是噪点）的右侧空白列。
            List01 = []
            List_Black = []
            List03 = []
            List01.append(i)
    return im

# 返回矩阵各行最大值位置的函数，以便找到有颜色的列中X轴投影最大的地方
def Max_Index(List1):
    Max = 0
    Max_index = 0
    for i in range(len(List1)):
        if len(List1[i]) > Max:
            Max = len(List1[i])
            Max_index = i
    return Max_index

# 返回矩阵各行最小值位置的函数，以便找到有颜色的列中X轴投影最小的地方
def Min_Index(List1):
    Min = 50
    Min_index = 0
    for i in range(len(List1)):
        if len(List1[i]) < Min:
            Min = len(List1[i])
            Min_index = i
    return Min_index

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

if __name__=='__main__':
    handle(os.path.join(os.path.dirname(__file__), 'img'), \
        os.path.join(os.path.dirname(__file__), 'pre_img'))