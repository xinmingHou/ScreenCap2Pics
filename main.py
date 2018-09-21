#!/usr/bin/env python
# encoding: utf-8
'''
@author: Xinming Hou
@license: (C) Copyright 2017-2018, CCNT of Zhejiang Unversity.
@contact: houxinming.chn@foxmail.com
@file: main.py
@time: 2018/9/20 下午3:48
@description:
'''

"""python + opencv 实现屏幕录制_by-_Zjh_"""
from PIL import ImageGrab
import numpy as np
import cv2
import time
import os

p = ImageGrab.grab() #获得当前屏幕
a, b = p.size #获得当前屏幕的大小

path = "screen/"

print("start print screen!")

while True:
    now_time = time.time()
    pic_path = os.path.join(path, str(now_time) + ".jpg")
    im = ImageGrab.grab()
    im = im.convert("RGB")

    im.save(pic_path)  # 保存

    # 25帧
    time.sleep(0.04)

