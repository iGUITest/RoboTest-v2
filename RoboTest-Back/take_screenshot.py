"""
Used to take screenshots of the screen of the device under test, and to correct and sharpen
"""
import cv2
import numpy as np


def take_screenshot(local_path, temp_picture, step, file_format, robo_step):
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    # get a frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imwrite(local_path + temp_picture + str(step) + file_format, frame)
    cap.release()
    cv2.destroyAllWindows()
    print('Successful screenshot!')
    print('take_screenshot:', local_path + temp_picture + str(step) + file_format)
    undistort_image(local_path + temp_picture + str(robo_step) + file_format)
    improve_image(local_path + temp_picture + str(robo_step) + file_format)


# camera correction
def undistort_image(input_file):
    parameter_mapping = {
        'internal_reference': [[503.942800, 0.000000, 306.128700],
                               [0.000000, 503.788500, 231.964800],
                               [0.000000, 0.000000, 1.000000]],
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
        print('Successful correction!')
    except:
        print('undistort error!')


# image sharpening
def improve_image(input_file):
    image = cv2.imread(input_file)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    dst = cv2.filter2D(image, -1, kernel=kernel)
    cv2.imencode('.jpg', dst)[1].tofile(input_file)
    print('Successful sharpening!')
