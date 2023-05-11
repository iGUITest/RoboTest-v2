"""
Used to judge whether there is a special-shaped screen occlusion bug during replay
"""
from opensource_code.cal_similarity import cal_similarity


def check_notch_bug(image_output_path, temp_picture, robo_step, file_format):
    target_output_file_path = image_output_path + temp_picture + str(robo_step) + file_format
    base_file_path = 'D:/iSE/2022_Summer/AutoArm/RoboTest/opensource_code/script/explore.robo/' + temp_picture + str(robo_step) + file_format
    img_similarity = cal_similarity(target_output_file_path, base_file_path)[0][0]
    if img_similarity < 0.3:
        print('Find a Notch BUG!')
        return True
    return False
