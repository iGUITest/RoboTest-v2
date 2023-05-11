"""
Used to perform script replay
"""
from opensource_code.atom_operation import create_text


def execute_replay(script_line, control_file_path):
    if script_line[0] == "slide":
        coordination = script_line[2]
        content = "slide "
        for coor in coordination:
            content = content + coor + " "
        create_text(control_file_path, content)
    else:
        coordination = script_line[2]
        x = coordination[0]
        y = coordination[1]
        content = script_line[0] + " " + str(x) + " " + str(y)
        print('*********************')
        print(content)
        print('*********************')
        create_text(control_file_path, content)
