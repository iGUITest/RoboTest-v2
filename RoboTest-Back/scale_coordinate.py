"""
Coordinate scaling calculation for cross-device replay
"""
import cv2


def scale_coordinate(old_x, old_y, old_picture, new_picture):
    print('****** old_x ******')
    print(old_x)
    print('*******************')
    print('****** old_y ******')
    print(old_y)
    print('*******************')
    old_img = cv2.imread(old_picture)
    new_img = cv2.imread(new_picture)
    old_length = old_img.shape[0]
    print('****** old_length ******')
    print(old_length)
    print('************************')
    old_width = old_img.shape[1]
    print('****** old_width ******')
    print(old_width)
    print('***********************')
    new_length = new_img.shape[0]
    print('****** new_length ******')
    print(new_length)
    print('************************')
    new_width = new_img.shape[1]
    print('****** new_width ******')
    print(new_width)
    print('***********************')
    global length, width
    new_phone_length = new_length / old_length * length
    new_phone_width = new_width / old_width * width
    x = (-(old_y - new_length)) / new_length * new_phone_width
    y = old_x / new_width * new_phone_length - new_phone_length / 2
    x = round(x, 4)
    y = round(y, 4)
    return x, y