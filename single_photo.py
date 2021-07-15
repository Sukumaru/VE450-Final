import cv2
import numpy as np
import os
import glob
import time

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# ret = cap.set(3, 320)
# ret = cap.set(4, 240)
# 设置摄像头分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


print(os.getcwd())

while cap.isOpened():
    ret, frame = cap.read()
    left_img = frame[:, 0:640, :]
    right_img = frame[:, 640:1280, :]
    if ret:
        # 显示两幅图片合成的图片·
        #
        cv2.imshow('img', frame)
        # 显示左摄像头视图
        cv2.imshow('left', left_img)
        # 显示右摄像头视图
        cv2.imshow('right', right_img)
    key = cv2.waitKey(delay=2)
    if key == ord('l'):
        cv2.imwrite('./photo' + str(1) + '.jpg', left_img)
        cv2.imwrite('./photo' + str(2) + '.jpg', right_img)
        i+=1
    if key == ord("q") or key == 27:
        break

cap.release()
