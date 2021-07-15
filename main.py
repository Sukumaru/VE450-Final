# import cv2
# import numpy as np
# import os
# import glob
# import time
#
# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# # ret = cap.set(3, 320)
# # ret = cap.set(4, 240)
# # 设置摄像头分辨率
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
# i = 0
# j = 0
#
# print(os.getcwd())
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     left_img = frame[:, 0:320, :]
#     right_img = frame[:, 320:640, :]
#     if ret:
#         # 显示两幅图片合成的图片·
#         #
#         cv2.imshow('img', frame)
#         # 显示左摄像头视图
#         cv2.imshow('left', left_img)
#         # 显示右摄像头视图
#         cv2.imshow('right', right_img)
#     key = cv2.waitKey(delay=2)
#     if key == ord('l'):
#         cv2.imwrite('./test_left' + str(i) + '.jpg', left_img)
#         cv2.imwrite('./test_right' + str(i) + '.jpg', right_img)
#         i+=1
#     if key == ord("q") or key == 27:
#         break
#
# cap.release()

import time
import cv2
import numpy as np
import os
from datetime import datetime

if __name__ == '__main__':
    try:

        # Photo session settings
        total_photos = 30             # Number of images to take
        countdown = 5                 # Interval for count-down timer, seconds
        font=cv2.FONT_HERSHEY_SIMPLEX # Cowntdown timer font

        # Camera settimgs
        cam_width = 1280
        cam_height = 480

        # Final image capture settings
        scale_ratio = 0.5
        # Camera resolution height must be dividable by 16, and width by 32
        print ("Used camera resolution: "+str(cam_width)+" x "+str(cam_height))


        # Initialize Camera 1 & Set height/width
        camera = cv2.VideoCapture(1)
        print("Setting the custom Width and Height")
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

        # # Initialize Camera 2 & Set height/width
        # camera2 = cv2.VideoCapture(1)
        # print("Setting the custom Width and Height")
        # camera2.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        # camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

        # Start Capturing Images
        counter = 0
        t2 = datetime.now()
        if (os.path.isdir("./pairs")==False):
          os.makedirs("./pairs")
        print ("Starting photo sequence")

        while True:
            # Read Camera 1
            check, frame = camera.read()
            frame1 = frame[:, 0:640, :]
            frame2 = frame[:, 640:1280, :]

            t1 = datetime.now()
            cntdwn_timer = countdown - int ((t1-t2).total_seconds())
            # If cowntdown is zero - let's record next image
            if cntdwn_timer == -1:
              counter += 1

              filename1 = './pairs/left_'+str(counter).zfill(2)+'.png'
              cv2.imwrite(filename1, frame1)
              filename2 = './pairs/right_'+str(counter).zfill(2)+'.png'
              cv2.imwrite(filename2, frame2)

              print (' ['+str(counter)+' of '+str(total_photos)+'] '+filename1)
              print (' ['+str(counter)+' of '+str(total_photos)+'] '+filename2)

              t2 = datetime.now()
              time.sleep(1)
              cntdwn_timer = 0      # To avoid "-1" timer display
              next
            # Draw cowntdown counter, seconds
            cv2.putText(frame1, str(cntdwn_timer), (50,50), font, 2.0, (0,0,255),4, cv2.LINE_AA)
            cv2.putText(frame2, str(cntdwn_timer), (50,50), font, 2.0, (0,0,255),4, cv2.LINE_AA)
            cv2.imshow("pair1", frame1)
            cv2.imshow("pair2", frame2)
            key = cv2.waitKey(1) & 0xFF

            # Wait till all photos are taken
            if (counter == total_photos):
              break

    except KeyboardInterrupt:
        camera.release()
        exit()