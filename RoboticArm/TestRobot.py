import cv2
import time
from move import *
import os

def get_photo(file_name, step, file_format): 
    cap = cv2.VideoCapture(-1)
    ret,frame = cap.read()
    if not ret:
        while True:
            GO = input('Continue? (yes/no): ')
            if GO == 'yes':
                break
        cap = cv2.VideoCapture(-1)
        ret, frame = cap.read()   
    image = "temp/" + file_name + str(step) + file_format
    cv2.imwrite(image,frame)

def get_flag(step):
    with open('temp/f' + str(step) + '.txt', 'w', encoding='utf-8') as f:
        f.close()

def is_exist_file(file_name, step):
    control_file_name = "temp/" + file_name + str(step) + ".txt"
    try:
        file = open(control_file_name,'r')
        file.close()
        return True
    except IOError:
        return False

import shutil

def delete_file(path):
    shutil.rmtree(path)

if __name__ == '__main__':
    file_name = 'picture'
    step = 1
    photo_step = 1
    file_format = '.jpg'
    #get_photo(file_name, step, file_format)
    get_flag(step)
    depth = 0.813    
    control = Control(depth)
    time.sleep(2)
    while (True):
        if photo_step == step:
        #     get_photo(file_name, photo_step, file_format)
            get_flag(step)
            photo_step += 1
        if is_exist_file(file_name, step):
            control_file_name = "temp/" + file_name + str(step) + ".txt"
            file = open(control_file_name, 'r')
            instruct = file.readline().split(" ")
            if instruct[0] == "click":
                control.click(float(instruct[1]), float(instruct[2]))
            elif instruct[0] == "double_click":
                control.double_click(float(instruct[1]), float(instruct[2]))
            elif instruct[0] == "long_click":
                control.long_click(float(instruct[1]), float(instruct[2]),3)
            elif instruct[0] == "slide":
                control.slide(float(instruct[1]), float(instruct[2]), float(instruct[3]), float(instruct[4]))
            elif instruct[0] == "end":
                print("end!")
                delete_file("/home/ubuntu/TestRobot/temp/")
                os.mkdir("temp")
                photo_step = 1
                step = 0
            step += 1
            #break
        else:
            print("not ready")

        time.sleep(5)
        
