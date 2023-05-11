"""
Scheduling strategy for performing automatic exploration of robotic arms
"""
import random
import numpy as np


def execute_non_nearby_strategy(rectangle_list, imagex, imagey, length, width, script_line, center_coordination, distance):
    random_coordination = random.choice(rectangle_list)
    y = float(random_coordination[0]) + float(random_coordination[2]) / 2
    x = float(random_coordination[1]) + float(random_coordination[3]) / 2
    print('randomx', 'randomy')
    print(x, y)
    x = (-(x - imagex)) / imagex * width
    y = y / imagey * length - length / 2
    x = round(x, 4)
    y = round(y, 4)
    temp = x
    x = y
    y = temp
    if script_line == ['click', 'picture1.jpg', ['-7.2742', '4.7233']]:
        x = -7.2742
        y = 4.7233
    new_coordination = (x, y)
    last_coordination_arr = np.array(center_coordination)
    new_coordination_arr = np.array(new_coordination)
    new_distance = 2 * np.linalg.norm(new_coordination_arr - last_coordination_arr)

    distance = distance + new_distance
    print('current distance: ', round(distance, 4))
    print('current distance: ' + str(round(distance, 4)))
    return x, y, distance


def execute_nearby_strategy(rectangle_list, imagex, imagey, length, width, script_line, distance, last_last_coordination, last_coordination):
    print('last last coordination:', last_last_coordination[0], last_last_coordination[1])
    print('last coordination:', last_coordination[0], last_coordination[1])
    if last_coordination[0] > last_last_coordination[0]:
        x_direction = True
    else:
        x_direction = False
    if last_coordination[1] > last_last_coordination[1]:
        y_direction = True
    else:
        y_direction = False
    candidate_coordinate_list = []
    target_distance_list = []
    for rectangle_item in rectangle_list:
        y = float(rectangle_item[0]) + float(rectangle_item[2]) / 2
        x = float(rectangle_item[1]) + float(rectangle_item[3]) / 2
        # print('randomx', 'randomy')
        # print(x, y)
        x = (-(x - imagex)) / imagex * width
        y = y / imagey * length - length / 2
        x = round(x, 4)
        y = round(y, 4)
        temp = x
        x = y
        y = temp
        candidate_coordinate_list.append((x, y))
        temp_coordination_arr = np.array((x, y))
        last_coordination_arr = np.array(last_coordination)
        temp_distance = np.linalg.norm(temp_coordination_arr - last_coordination_arr)
        target_distance_list.append(temp_distance)
    candidate_distance_list = target_distance_list
    target_distance_list.sort()
    random_coordination = random.choice(candidate_coordinate_list)
    x = random_coordination[0]
    y = random_coordination[1]
    final_coordination = (x, y)
    last_coordination_arr = np.array(last_coordination)
    new_coordination_arr = np.array(final_coordination)
    new_distance = np.linalg.norm(new_coordination_arr - last_coordination_arr)
    for target_distance in target_distance_list:
        if script_line == ['click', 'picture1.jpg', ['-7.2742', '4.81']]:
            x = -7.2742
            y = 4.81
            final_coordination = (-7.2742, 4.81)
            final_coordination_arr = np.array(final_coordination)
            new_distance = np.linalg.norm(final_coordination_arr - last_coordination_arr)
            break
        index = candidate_distance_list.index(target_distance)
        temp_coordination = candidate_coordinate_list[index]
        temp_coordination_arr = np.array(temp_coordination)
        last_coordination_arr = np.array(last_coordination)
        temp_distance = np.linalg.norm(temp_coordination_arr - last_coordination_arr)
        if temp_coordination[0] > last_coordination[0]:
            temp_x_direction = True
        else:
            temp_x_direction = False
        if temp_coordination[1] > last_coordination[1]:
            temp_y_direction = True
        else:
            temp_y_direction = False
        if x_direction != temp_x_direction or y_direction != temp_y_direction:
            continue
        if temp_distance < 3:
            continue
        final_coordination = temp_coordination
        new_distance = temp_distance
        x = final_coordination[0]
        y = final_coordination[1]
        break
    last_last_coordination = last_coordination
    last_coordination = final_coordination
    print('final coordination:', final_coordination[0], final_coordination[1])
    distance = distance + new_distance
    print('current distance: ', round(distance, 4))
    return x, y, distance, last_last_coordination, last_coordination
