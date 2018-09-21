#!/usr/bin/env python
# encoding: utf-8
'''
@author: Xinming Hou
@license: (C) Copyright 2017-2018, CCNT of Zhejiang Unversity.
@contact: houxinming.chn@foxmail.com
@file: findPix.py
@time: 2018/6/4 下午9:54
@description:
'''

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton,  QTextBrowser
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5 import QtCore
from PIL import ImageGrab

import time
import os




class ScreenCap(QWidget):
    def __init__(self):
        super().__init__()
        self.path = "screen/"

        self.p = ImageGrab.grab()  # 获得当前屏幕
        self.rx, self.ry = self.p.size  # 获得当前屏幕的大小
        self.lx = 0
        self.ly = 0
        self.framerate = 30

        self.pickleft = True
        self.is_pick = False

        self.timer = QtCore.QTimer()

        self.initUI()
        self.slot()
        self.setWindowTitle('Screen Cap')
        self.show()

    def initUI(self):

        layout_all = QVBoxLayout()

        grid_loc = QGridLayout()

        lb_left_up = QLabel("左上角坐标：")
        lb_right_up = QLabel("右下角坐标：")
        lb_x = QLabel("X")
        lb_y = QLabel("Y")

        self.edit_lx = QLineEdit(str(self.lx))
        self.edit_ly = QLineEdit(str(self.ly))

        self.edit_rx = QLineEdit(str(self.rx))
        self.edit_ry = QLineEdit(str(self.ry))

        grid_loc.addWidget(lb_left_up, 1, 0)
        grid_loc.addWidget(lb_right_up, 2, 0)
        grid_loc.addWidget(lb_x, 0, 1)
        grid_loc.addWidget(lb_y, 0, 2)
        grid_loc.addWidget(self.edit_lx, 1, 1)
        grid_loc.addWidget(self.edit_ly, 1, 2)
        grid_loc.addWidget(self.edit_rx, 2, 1)
        grid_loc.addWidget(self.edit_ry, 2, 2)

        layout_all.addLayout(grid_loc)

        layout_pick = QHBoxLayout()
        self.bt_allscreen = QPushButton("全屏")
        self.bt_pickloc = QPushButton("屏幕选点")
        layout_pick.addWidget(self.bt_pickloc)
        layout_pick.addWidget(self.bt_allscreen)

        layout_all.addLayout(layout_pick)

        # 帧率
        layout_frame = QHBoxLayout()

        lb_framerate = QLabel("帧率")
        self.edit_framerate = QLineEdit(str(self.framerate))

        layout_frame.addWidget(lb_framerate, 1)
        layout_frame.addWidget(self.edit_framerate, 3)

        layout_all.addLayout(layout_frame)

        # 时间
        layout_time = QHBoxLayout()

        lb_time = QLabel("时间")
        lb_timecontent = QLabel("没计时器")

        layout_time.addWidget(lb_time, 1)
        layout_time.addWidget(lb_timecontent, 3)

        layout_all.addLayout(layout_time)

        # 文件日志
        lb_filename = QLabel("文件日志：")
        self.browser_file = QTextBrowser()

        layout_all.addWidget(lb_filename)
        layout_all.addWidget(self.browser_file)

        self.bt_REC = QPushButton("开始录制")
        layout_all.addWidget(self.bt_REC)


        self.setLayout(layout_all)



    def slot(self):
        self.bt_allscreen.clicked.connect(self.setallscreen)
        self.bt_pickloc.clicked.connect(self.setpick)
        self.bt_REC.clicked.connect(self.begin_rec)

        self.timer.timeout.connect(self.rec)

    def mousePressEvent(self, event):
        if self.is_pick:
            if self.pickleft:
                self.lx = event.globalX()
                self.ly = event.globalY()
                self.edit_lx.setText(str(self.lx))
                self.edit_ly.setText(str(self.ly))
            else:
                self.rx = event.globalX()
                self.ry = event.globalY()
                self.edit_rx.setText(str(self.rx))
                self.edit_ry.setText(str(self.ry))

    def mouseReleaseEvent(self, event):
        if self.is_pick:
            if self.pickleft:
                self.pickleft = False
            else:
                self.pickleft = True
                self.is_pick = False
                self.bt_pickloc.setText("屏幕选点")

    def setpick(self):
        if self.is_pick == False:
            self.is_pick = True
            self.bt_pickloc.setText("正在选点")
        else:
            self.is_pick = False
            self.bt_pickloc.setText("屏幕选点")

    def setallscreen(self):
        self.rx, self.ry = self.p.size

    def begin_rec(self):
        if self.timer.isActive() == False:
            # 获取设置的参数
            t = 1000/self.framerate
            self.lx = int(self.edit_lx.text())
            self.ly = int(self.edit_ly.text())
            self.rx = int(self.edit_rx.text())
            self.ry = int(self.edit_ry.text())

            self.timer.start(t)
            self.bt_REC.setText(u'停止录制')
        else:
            self.timer.stop()
            self.bt_REC.setText(u'开始录制')

    def rec(self):
        now_time = time.time()
        pic_path = os.path.join(self.path, str(now_time) + ".jpg")
        loc = (self.lx,self.ly,self.rx,self.ry)
        im = ImageGrab.grab(loc)
        im = im.convert("RGB")
        im.save(pic_path)  # 保存







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenCap()
    sys.exit(app.exec_())



