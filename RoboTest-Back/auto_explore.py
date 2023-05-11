"""
Used to perform robotic arm automation exploration
"""
import shutil
import cv2
from opensource_code.atom_operation import create_text
from opensource_code.scheduling_strategy import execute_non_nearby_strategy, execute_nearby_strategy
from opensource_code.widget_extraction import extract_widgets


def auto_explore(script_line, control_file_path, robo_step, cut_output_file_path, image_output_path, temp_picture, file_format,
                 length, width, center_coordination, distance, last_last_coordination, last_coordination):
    if script_line[0] == "slide":
        coordination = script_line[2]
        content = "slide "
        for coor in coordination:
            content = content + coor + " "
        create_text(control_file_path, content)
        content_modify = 'slide("picture' + str(robo_step) + '.jpg") '
        for coor in coordination:
            content_modify = content_modify + coor + " "
        f_new = open(r"D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\script\explore.robo\explore.txt", "a",
                     encoding="UTF-8")
        print('content_modify:', content_modify)
        f_new.write(content_modify + '\n')
        f_new.close()
        shutil.copy(cut_output_file_path, r"D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\script\explore.robo")
    else:
        # TODO
        print('script_line')
        print(script_line)
        image = cv2.imread(image_output_path + temp_picture + str(robo_step) + file_format)
        print('image')
        print(image_output_path + temp_picture + str(robo_step) + file_format)
        rectangle_list = extract_widgets(image, color=(0, 0, 255))
        imagex, imagey = cv2.imread(cut_output_file_path).shape[:2]
        print('imagex', 'imagey')
        print(imagex, imagey)

        # choose non_nearby strategy or nearby strategy
        x, y, distance = execute_non_nearby_strategy(rectangle_list, imagex, imagey, length, width, script_line,
                                                     center_coordination, distance)
        # x, y, distance, last_last_coordination, last_coordination = execute_nearby_strategy(rectangle_list, imagex, imagey, length, width, script_line, distance, last_last_coordination, last_coordination)

        content = script_line[0] + " " + str(x) + " " + str(y)
        print('*********************')
        print(content)
        print('*********************')
        create_text(control_file_path, content)
        content_modify = script_line[0] + '("picture' + str(robo_step) + '.jpg") ' + str(x) + " " + str(y)
        f_new = open(r"D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\script\explore.robo\explore.txt", "a",
                     encoding="UTF-8")
        print('content_modify:', content_modify)
        f_new.write(content_modify + '\n')
        f_new.close()
        shutil.copy(cut_output_file_path,
                    r"D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\script\explore.robo")
    return distance, last_last_coordination, last_coordination
