"""
用于对被测设备屏幕进行拍摄截图，以及矫正锐化
"""
import cv2
import numpy as np


def take_screenshot(img_name):
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)  # 打开摄像头
    # get a frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示
    cv2.imwrite('image/' + img_name, frame)  # 保存路径
    cap.release()
    cv2.destroyAllWindows()
    print('截图成功！')
    undistort_image('image/' + img_name)
    improve_image('image/' + img_name)


# 摄像头矫正
def undistort_image(input_file):
    parameter_mapping = {
        # 内参
        'internal_reference': [[503.942800, 0.000000, 306.128700],
                               [0.000000, 503.788500, 231.964800],
                               [0.000000, 0.000000, 1.000000]],
        # 畸变
        'distortion': [-0.4996, 0.2711, 0.000000, 0.000000, 0.000000]
    }
    target_img = cv2.imread(input_file)
    flip_horizontal = cv2.flip(target_img, 1)
    cv2.imwrite(input_file, flip_horizontal)
    try:
        img = cv2.imdecode(np.fromfile(input_file, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(np.array(parameter_mapping["internal_reference"]),
                                                          np.array(parameter_mapping["distortion"]), (w, h), 1,
                                                          (w, h))
        dst = cv2.undistort(img, np.array(parameter_mapping["internal_reference"]),
                            np.array(parameter_mapping["distortion"]), None, newcameramtx)
        cv2.imencode('.jpg', dst)[1].tofile(input_file)
        print('矫正成功！')
    except:
        print('undistort error!')


# 图像锐化
def improve_image(input_file):
    image = cv2.imread(input_file)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    dst = cv2.filter2D(image, -1, kernel=kernel)
    cv2.imencode('.jpg', dst)[1].tofile(input_file)
    print('锐化成功！')


take_screenshot('1.jpg')
