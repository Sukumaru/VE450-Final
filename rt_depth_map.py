import cv2
import numpy as np
from stereovision.calibration import StereoCalibration
from datetime import datetime


def stereo_estimate(sbm, rectified_pair, Q, target_x, target_y):
    # Calculate Disparity
    dmLeft = rectified_pair[0]
    dmRight = rectified_pair[1]
    disparity = sbm.compute(dmLeft, dmRight)

    points_3d = cv2.reprojectImageTo3D(disparity, Q)
    print(points_3d.shape())

    # Filter Disparity Estimate
    local_max = disparity.max()
    local_min = disparity.min()
    disparity_grayscale = (disparity - local_min) * (65535.0 / (local_max - local_min))
    disparity_fixtype = cv2.convertScaleAbs(disparity_grayscale, alpha=(255.0 / 65535.0))
    disparity_color = cv2.applyColorMap(disparity_fixtype, cv2.COLORMAP_JET)

    # Disparity Array Values
    disparity_estimate = np.delete(disparity_fixtype, np.s_[:50], 1)
    disparity_estimate = np.delete(disparity_estimate, np.s_[250:340], 1)
    disparity_estimate = np.delete(disparity_estimate, np.s_[:20], 0)

    average = np.average(disparity_estimate)
    pixel_percentage = np.count_nonzero(disparity_estimate > 127.5) / 55000

    print(average, pixel_percentage)
    detected = average > 70.34 and pixel_percentage > .35

    print("Object Detected:" + str(detected), "Average" + str(average),
          "Percentage of Pixels Above Threshold:" + str(pixel_percentage))

    cv2.imshow("Image", disparity_color)
    #cv2.putText(frame1, str(cntdwn_timer), (50, 50), font, 2.0, (0, 0, 255), 4, cv2.LINE_AA)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        quit()
    return detected


if __name__ == '__main__':
    try:

        # Camera settings
        cam_width = 1280
        cam_height = 480

        # Final image capture settings
        scale_ratio = 0.5
        # Camera resolution height must be dividable by 16, and width by 32
        print("Used camera resolution: " + str(cam_width) + " x " + str(cam_height))

        # Buffer for captured image settings
        img_width = int (cam_width * scale_ratio)
        img_height = cam_height
        capture = np.zeros((img_height, img_width, 4), dtype=np.uint8)
        print ("Scaled image resolution: "+str(img_width)+" x "+str(img_height))

        camera = cv2.VideoCapture(1)
        print("Setting the custom Width and Height")
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

        # camera2 = cv2.VideoCapture(2)
        # print("Setting the custom Width and Height")
        # camera2.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        # camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

        # Implementing calibration data
        print('Read calibration data and rectifying stereo pair...')
        calibration = StereoCalibration(input_folder='calib_result')

        left_K = calibration.cam_mats["left"]
        right_K = calibration.cam_mats["right"]
        left_distortion = calibration.dist_coefs["left"]
        right_distortion = calibration.dist_coefs["right"]
        R = calibration.rot_mat
        T = calibration.trans_vec

        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(left_K, left_distortion, right_K, right_distortion,
                                                          (640, 480), R, T, alpha=0)


        # Initialize interface windows
        cv2.namedWindow("Image")
        cv2.moveWindow("Image", 50, 100)
        cv2.namedWindow("left")
        cv2.moveWindow("left", 450, 100)
        cv2.namedWindow("right")
        cv2.moveWindow("right", 850, 100)

        disparity = np.zeros((img_width, img_height), np.uint8)
        sbm = cv2.StereoBM_create(numDisparities=0, blockSize=21)

        while True:
            # Read Camera 1
            check, frame = camera.read()
            frame1 = frame[:, 0:640, :]
            frame2 = frame[:, 640:1280, :]

            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            t1 = datetime.now()
            imgLeft = frame1
            imgRight = frame2
            rectified_pair = calibration.rectify((imgLeft, imgRight))
            target_x = 100
            target_y = 100
            object_detected = stereo_estimate(sbm, rectified_pair,Q, target_x,target_y)

            # show the frame
            cv2.imshow("left", imgLeft)
            cv2.imshow("right", imgRight)

            t2 = datetime.now()
            print("DM build time: " + str(t2 - t1))

    except KeyboardInterrupt:
        camera.release()
        exit()