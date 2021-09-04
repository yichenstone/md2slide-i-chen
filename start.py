import os
import sys

try:
    a = sys.argv[1]
    print("正在转换，请稍候……")
    d = os.popen("python e:\python项目\markdown2slide_v1.0\md2slide.py "+a)
    print(d.read())
    print("转换完成")
except BaseException as e:
    a =input("请输入md文件路径（例 D:\我的md文件\myslide.md）：")
    print("正在转换，请稍候……")
    d = os.popen("python e:\python项目\markdown2slide_v1.0\md2slide.py " + a)
    print(d.read())
    print("转换完成")
input()