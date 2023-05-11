"""
Used to clean up temporary files before starting the backend of the robotic arm each time
"""
import os


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


del_file(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\image\flag')
del_file(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\image\input')
del_file(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\image\output')
del_file(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\control')
del_file(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\script\explore.robo')
open(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\script\explore.robo\explore.txt', 'w').close()
