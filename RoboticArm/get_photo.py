import cv2
import time
import os

def get_photo(file_name, step, file_format): 
    cap = cv2.VideoCapture(-1)
    ret,frame = cap.read()
    image = "temp/" + file_name + str(step) + file_format
    cv2.imwrite(image,frame)

if __name__ == '__main__':
    file_name = 'picture'
    step = 1
    photo_step = 1
    file_format = '.jpg'
    while step < 2:
        get_photo(file_name, step, file_format)
        step += 1
        time.sleep(2)
