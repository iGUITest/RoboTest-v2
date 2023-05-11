"""
Used to generate atomic operations to control the robotic arm
"""
import cv2


def generate_instructions(control_file_path, length, width, imagex, imagey, a, b, output_file_path, raw_file_path):
    image = cv2.imread(output_file_path)
    print(output_file_path)
    if len(a) == 1:  # click

        coordinate = [b[0], a[0]]
        cv2.imwrite(raw_file_path, image)

        x = (-(a[0] - imagex)) / imagex * width
        y = b[0] / imagey * length - length / 2
        x = round(x, 4)
        y = round(y, 4)
        control = "click " + str(y) + " " + str(x)
        print("click {},{}".format(x, y))
    elif len(a) == 3:  # long_click
        x = (-(a[0] - imagex)) / imagex * width
        y = b[0] / imagey * length - length / 2
        x = round(x, 4)
        y = round(y, 4)
        control = "long_click " + str(y) + " " + str(x)
        print("long click {},{}".format(x, y))
    elif abs(a[0] - a[1]) < 10 and abs(b[0] - b[1]) < 10:  # double_click
        x = (-(a[0] - imagex)) / imagex * width
        y = b[0] / imagey * length - length / 2
        x = round(x, 4)
        y = round(y, 4)
        control = "double_click " + str(y) + " " + str(x)
        print("double click {},{}".format(x, y))
    else:  # scroll
        x1 = (-(a[0] - imagex)) / imagex * width
        y1 = b[0] / imagey * length - length / 2
        x2 = (-(a[1] - imagex)) / imagex * width
        y2 = b[1] / imagey * length - length / 2
        x1 = round(x1, 4)
        y1 = round(y1, 4)
        x2 = round(x2, 4)
        y2 = round(y2, 4)
        control = "slide " + str(y1) + " " + str(x1) + " " + str(y2) + " " + str(x2)
        print("slide {},{} -> {},{}".format(x1, y1, x2, y2))
    print(control_file_path)
    print(control)
    create_text(control_file_path, control)
    print("leave generate_control_instructions")
    return control


def create_text(name, msg):
    full_path = name
    file = open(full_path, 'w')
    print(msg)
    file.write(msg)
    file.close()
