"""
Used to start the backend of the RoboTest
"""
import base64
import glob
import json
import logging
import os
import shutil
import threading
import time
import paramiko
from flask import Flask, request, make_response
from flask_cors import CORS
from cut import *
from image_matching import *
from opensource_code.atom_operation import generate_instructions, create_text
from opensource_code.auto_explore import auto_explore
from opensource_code.notch_check import check_notch_bug
from opensource_code.screen_recognition import PhoneDet
from opensource_code.script_replay import execute_replay
from opensource_code.transfer_with_autoarm import send_to_autoarm, get_from_autoarm
from tools.monkey import generate_monkey
from shutil import copyfile
from take_screenshot import take_screenshot

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

global a
global b

global phone_size

# The length, width and height of the mobile phone
global height
global width
global length

# robot connect
global host_ip
global username
global password
# robotic arm address and local address
global remote_path
global local_path

# image and script storage address
global image_input_path
global image_output_path
global file_name
global file_format
global control_base_path

# consistency variable
global step
global robo_step
global temp_picture
global script_name
global is_replay


def set_ubuntu_connect(h_ip, uname, passw):
    global host_ip, username, password
    host_ip = h_ip
    username = uname
    password = passw


def set_phone_parameter(l, w, h):
    global length, width, height
    length = l
    width = w
    height = h


def set_location(input_path, output_path, r_path, l_path, c_base_path):
    global image_input_path, image_output_path, remote_path, local_path, control_base_path
    image_input_path = input_path
    image_output_path = output_path
    remote_path = r_path
    local_path = l_path
    control_base_path = c_base_path


def set_file(f_name, f_format, script_path):
    global file_name, file_format, script_base_path
    file_name = f_name
    file_format = f_format
    script_base_path = script_path


def generate_monkey_coordination(length, width, imagex, imagey):
    global a, b
    logging.info("enter generate_monkey_coordination")
    x = (-(a[0] - imagex)) / imagex * width
    y = b[0] / imagey * length - length / 2
    x = round(x, 4)
    y = round(y, 4)
    return x, y


# accept the operation parameters passed by the front end, generate operation instructions, and generate scripts
@app.route('/get_control', methods=['GET', 'POST'])
def get_from_front():
    control_data = {
        "data": {},
        "meta": {},
    }
    global a, b, control_base_path, file_name, step, length, width, script_base_path, temp_picture, photo_step
    recv_data = request.get_data()
    if recv_data:
        json_re = json.loads(recv_data)
    else:
        logging.exception("receive data is empty: get_control")
        control_data['meta']['status'] = '400'
        return json.dumps(control_data)
    a = json_re["YList"]
    b = json_re["XList"]
    imagey = json_re["lengthX"]
    imagex = json_re["lengthY"]

    # imagex indicates the vertical width of the image
    # imagey indicates the horizontal width of the image
    # a indicates the vertical coordinate
    # b indicates the horizontal coordinate
    print(a, b, imagex, imagey)

    control_file_path = control_base_path + temp_picture + str(step) + ".txt"
    script_dir = script_base_path + file_name + ".robo/"
    script_file_path = script_dir + file_name + ".txt"

    global image_output_path, file_format

    output_file_path = image_output_path + 'picture' + str(robo_step - 1) + file_format
    raw_file_path = image_output_path + 'picture' + str(robo_step - 1) + '_raw' + file_format
    control = generate_instructions(control_file_path, length, width, imagex, imagey, a, b, output_file_path, raw_file_path)

    control = control.split(" ")[0] + "(\"picture" + str(step) + ".jpg\") " + " ".join(control.split(" ")[1:])

    # write into script
    try:
        fp = open(script_file_path, 'a', encoding='utf-8')
        fp.write('\n')
        fp.write(control)
        fp.close()
    except IOError:
        fp = open(script_file_path, 'w', encoding='utf-8')
        fp.write(control)
        fp.close()
    origin_path = image_output_path + temp_picture + str(step) + file_format
    origin_raw_path = image_output_path + temp_picture + str(step) + '_raw' + file_format
    target_path = script_dir + temp_picture + str(step) + file_format
    target_base_path = script_dir + "base/"
    copyfile(origin_path, target_path)
    shutil.copy(origin_raw_path, target_base_path)
    src = control_file_path
    des = remote_path + temp_picture + str(step) + '.txt'
    step = step + 1
    send_to_autoarm(src, des)
    photo_step = photo_step + 1
    control_data['meta']['status'] = '200'
    return json.dumps(control_data)


# start recording and initialize
@app.route('/begin_record', methods=['GET', 'POST'])
def begin_record():
    path = {
        "data": {},
    }
    recv_data = request.get_data()
    if recv_data:
        json_re = json.loads(recv_data)
    else:
        logging.exception("receive data is empty: begin_record")
        path['data']['status'] = '400'
        return json.dumps(path)

    # accept the parameters of the front end and create the corresponding folder
    script_name = json_re["scriptName"]
    create_script_dir(script_name)

    global step, image_output_path, file_name, file_format
    file_name = script_name
    path['data']['step'] = step
    path['data']['file_name'] = file_name
    path['data']['image_output_path'] = image_output_path
    path['data']['file_format'] = file_format
    return json.dumps(path)


# end the recording function and clear the temporary files
@app.route('/end_record', methods=['GET', 'POST'])
def end_record():
    global image_input_path, image_output_path, control_base_path
    global step, robo_step, file_name

    control_file_path = control_base_path + "picture" + str(robo_step) + ".txt"
    content = "end "
    create_text(control_file_path, content)

    try:
        t = paramiko.Transport((host_ip, 22))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        src = remote_path + temp_picture + str(step) + '.txt'
        des = control_file_path
        sftp.put(des, src)
        t.close()
    except Exception as e:
        logging.exception("upload file error: {}".format(src))

    # delete temporary files
    delete_file(image_input_path)
    delete_file(image_output_path)
    delete_file(control_base_path)

    step = 1
    file_name = ''
    return str(200)


@app.route('/monkey', methods=['GET', 'POST'])
def monkey():
    path = {
        "data": {},
    }
    recv_data = request.get_data()
    if recv_data:
        json_re = json.loads(recv_data)
    else:
        logging.exception("receive data is empty: monkey")
        path['data']['status'] = '400'
        return json.dumps(path)

    # accept the parameters of the front end and create the corresponding folder
    monkey_time = int(json_re["monkey_time"])
    left_bottom_input = json_re['left_bottom']
    right_top_input = json_re['right_top']
    left_bottom_list = left_bottom_input.split(',')
    right_top_list = right_top_input.split(',')
    left_bottom = []
    right_top = []
    for item in left_bottom_list:
        left_bottom.append(eval(item))
    for item in right_top_list:
        right_top.append(eval(item))
    print(monkey_time)
    print(left_bottom)
    print(right_top)
    generate_monkey(monkey_time, left_bottom, right_top)
    return make_response('monkey create ok')


def delete_file(path):
    # read all the files under the folder
    file_names = glob.glob(path + r'\*')

    for file_name in file_names:
        try:
            os.remove(file_name)
        except:
            try:
                os.rmdir(file_name)
            except:
                delete_file(file_name)
                os.rmdir(file_name)


# create a script folder to store script files and pictures
def create_script_dir(script_name):
    global script_base_path
    script_dir = script_base_path + script_name + ".robo/"
    base_dir = script_base_path + script_name + ".robo/base/"

    if os.path.exists(script_dir):
        pass
    else:
        os.mkdir(script_dir)
    if os.path.exists(base_dir):
        pass
    else:
        os.mkdir(base_dir)


# get script file content
@app.route('/get_script_file', methods=['GET', 'POST'])
def get_script_file():
    global file_name, script_base_path
    script_dir = script_base_path + file_name + ".robo/"
    script_file_path = script_dir + file_name + ".txt"
    fp = open(script_file_path, 'r', encoding='utf-8')
    script = fp.read()
    fp.close()
    return script


# save script file
@app.route('/editscript_save', methods=['GET', 'POST'])
def editscript_save():
    recv_data = request.get_data()
    if recv_data:
        json_re = json.loads(recv_data)
    else:
        logging.exception("receive data is empty: editscript_save")
        return str(400)

    script_content = json_re["content"]
    global script_name, script_base_path
    script_dir = script_base_path + script_name + ".robo/"
    script_file_path = script_dir + script_name + ".txt"
    fp = open(script_file_path, 'w', encoding='utf-8')
    fp.write(script_content)
    fp.close()
    return str(200)


# get the script file and parse it into sikuli's text and picture mode
@app.route('/get_script_data', methods=['GET', 'POST'])
def get_script_data():
    recv_data = request.get_data()
    if recv_data:
        json_re = json.loads(recv_data)
    else:
        logging.exception("receive data is empty: get_script_data")
        return str(400)

    # get the name of the file currently being processed and modify it
    front_script_name = json_re["scriptName"]
    global script_name, script_base_path
    script_name = front_script_name
    script_dir = script_base_path + script_name + ".robo/"
    script_file_path = script_dir + script_name + ".txt"
    fp = open(script_file_path, 'r', encoding='utf-8')
    file = fp.read()
    file = file.split("\n")
    script = []
    for line in file:
        if line == '':
            continue
        this_line = []
        lines = line.split('(')
        this_line.append(lines[0])
        lines = lines[1]
        lines = lines.split(')')
        lines[0] = lines[0].replace("\"", "")
        # convert image links to image storage
        img = str(return_img_stream(script_dir + lines[0]))
        img = img[2:-1]
        this_line.append(img)
        lines = lines[1]
        lines = lines.split(' ')
        this_line.append(lines[1:])
        script.append(this_line)
    fp.close()
    return json.dumps(script)


# return picture stream data
def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


# get picture
@app.route('/get_picture', methods=['GET', 'POST'])
def get_picture():
    global step, image_output_path, temp_picture, file_format
    path = image_output_path + temp_picture + str(step) + file_format

    data = return_img_stream(path)
    return data


# determine whether the robotic arm takes the current picture (whether the picture exists)
@app.route('/exist_img', methods=['GET', 'POST'])
def exist_img():
    global step
    front_step = request.args.get('step')
    if int(front_step) == step:
        return str(200)
    else:
        return str(400)


# in the replay stage, judge whether the robotic arm captures the current picture (whether the picture exists)
@app.route('/exist_replay_img', methods=['GET', 'POST'])
def exist_img2():
    global robo_step
    front_step = request.args.get('step')
    if int(front_step) == robo_step:
        return str(200)
    else:
        return str(400)


# script editing interface, save the script
@app.route('/save_screenshot', methods=['GET', 'POST'])
def save_screenshot():
    recv_data = request.get_data()
    if recv_data:
        json_re = json.loads(recv_data)

    else:
        logging.exception("receive data is empty: save_screenshot")
        return str(400)
    global script_base_path, script_name
    script_dir = script_base_path + script_name + ".robo/"
    screenshot_name = json_re["imgName"]
    screenshotURI = json_re["screenshotURI"]

    # the length and width of the new picture after screenshot, used for cropping
    height = json_re["height"]
    width = json_re["width"]

    # Save pictures on canvas
    screenshotURI = screenshotURI.split(',')[1]
    screenshotURI = base64.b64decode(screenshotURI)
    with open(script_dir + screenshot_name + '.jpg', 'wb') as f:
        f.write(screenshotURI)
    img = cv2.imread(script_dir + screenshot_name + '.jpg')
    cut_img = img[0:height, 0:width]
    cv2.imwrite(script_dir + screenshot_name + '.jpg', cut_img)
    return str(200)


# start replay and initialize
global script_lines


@app.route('/run_replay', methods=['GET', 'POST'])
def run_replay():
    global is_replay
    is_replay = True
    global script_name, script_base_path
    script_dir = script_base_path + script_name + ".robo/"
    script_file_path = script_dir + script_name + ".txt"
    fp = open(script_file_path, 'r', encoding='utf-8')
    file = fp.read()
    file = file.split("\n")
    script = []
    for line in file:
        if line == '':
            continue
        this_line = []
        lines = line.split('(')
        this_line.append(lines[0])
        lines = lines[1]
        lines = lines.split(')')
        lines[0] = lines[0].replace("\"", "")
        this_line.append(lines[0])
        lines = lines[1]
        lines = lines.split(' ')
        this_line.append(lines[1:])
        script.append(this_line)
    fp.close()
    global script_lines
    script_lines = script
    return str(200)


global control_img


class TestRobot(object):
    def __init__(self, image_input_path, image_output_path, remote_path, local_path):
        # image path
        self.height = None
        self.width = None
        self.length = None
        self.image_input_path = image_input_path
        self.image_output_path = image_output_path
        self.host_ip = '192.168.101.10'
        self.username = 'ubuntu'
        self.password = 'hiwonder'
        self.remote_path = remote_path
        self.local_path = local_path

    def get_phone_parameter(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    # image comparison
    def findCoodination(self, script_picture_path, output_picture_path):
        coordination = exec(script_picture_path, output_picture_path)
        return coordination


def robotest():
    global robo_step, file_name, temp_picture, is_replay, phone_size, local_path, file_format, photo_step

    while True:
        while file_name == '' and is_replay is False:
            robo_step = 1
            time.sleep(1)
        if file_name != '':
            src = TestRobot.remote_path + 'f' + str(robo_step) + '.txt'
            des = flag_path + 'f' + str(robo_step) + '.txt'
            if get_from_autoarm(src, des):
                take_screenshot(local_path, temp_picture, step, file_format, robo_step)
                logging.info("record service start")
                # recode operation
                cut_file_path = image_input_path + temp_picture + str(robo_step) + file_format
                cut_output_file_path = image_output_path + temp_picture + str(robo_step) + file_format
                target_output_file_path = image_output_path + temp_picture + str(robo_step) + '_raw' + file_format

                img_target = cv2.imread(cut_file_path)
                phone_size = PhoneDet(cut_output_file_path, image=img_target, info=phone_size)
                print('phone_size')
                print(phone_size)

                robo_step += 1
                # break
            else:
                logging.info("ERROR: AUTOARM NOT READY")
            time.sleep(5)
        else:  # replay
            logging.info("replay service start")
            global script_lines, control_base_path, bottom_center_coordination, distance, last_coordination, last_last_coordination
            # when the replay ends, set the end flag
            if robo_step > len(script_lines):
                control_file_path = control_base_path + str(robo_step) + ".txt"
                content = "end "
                create_text(control_file_path, content)
                is_replay = False
                src = control_file_path
                des = TestRobot.remote_path + 'picture' + str(robo_step) + '.txt'
                send_to_autoarm(src, des)
            else:
                src = TestRobot.remote_path + 'f' + str(robo_step) + '.txt'
                des = flag_path + 'f' + str(robo_step) + '.txt'
                if get_from_autoarm(src, des):
                    print('get ' + local_path + temp_picture + str(robo_step) + file_format)
                    take_screenshot(local_path, temp_picture, robo_step, file_format, robo_step)
                    # recode operation
                    cut_file_path = image_input_path + temp_picture + str(robo_step) + file_format
                    cut_output_file_path = image_output_path + temp_picture + str(robo_step) + file_format

                    img_target = cv2.imread(cut_file_path)
                    phone_size = PhoneDet(cut_output_file_path, image=img_target, info=phone_size)
                    print('phone_size')
                    print(phone_size)
                    control_file_path = control_base_path + str(robo_step) + ".txt"
                    script_line = script_lines[robo_step - 1]
                    print('script_line:', script_line)
                    print('script_line[0]:', script_line[0])
                    print('script_line[1]:', script_line[1])
                    print('script_line[2]:', script_line[2])
                    logging.info('Current execution times: ' + str(robo_step))
                    global script_name, script_base_path

                    command = 'replay'
                    if command == 'replay':
                        execute_replay(script_line, control_file_path)
                        # x = x * new_length / old_length
                        # y = y * new_width / old_width
                    elif command == 'explore':
                        distance, last_last_coordination, last_coordination = auto_explore(script_line, control_file_path, robo_step, cut_output_file_path, image_output_path,
                                     temp_picture, file_format,
                                     length, width, center_coordination, distance, last_last_coordination,
                                     last_coordination)
                    src = control_file_path
                    des = TestRobot.remote_path + "picture" + str(robo_step) + '.txt'
                    send_to_autoarm(src, des)

                    ifJudgeNotch = True
                    if ifJudgeNotch:
                        ifCatchNotchBug = check_notch_bug(image_output_path, temp_picture, robo_step, file_format)
                    robo_step += 1
                    # break
                else:
                    logging.info("error: cannot capture the screenshot")

                time.sleep(5)


if __name__ == '__main__':
    step = 1
    image_input_path = 'D:/iSE/2022_Summer/AutoArm/RoboTest/opensource_code/image/input/'
    image_output_path = 'D:/iSE/2022_Summer/AutoArm/RoboTest/opensource_code/image/output/'
    remote_path = '/home/ubuntu/TestRobot/temp/'
    local_path = 'D:/iSE/2022_Summer/AutoArm/RoboTest/opensource_code/image/input/'
    flag_path = 'D:/iSE/2022_Summer/AutoArm/RoboTest/opensource_code/image/flag/'
    control_base_path = 'D:/iSE/2022_Summer/AutoArm/RoboTest/opensource_code/control/'
    script_base_path = 'D:/iSE/2022_Summer/AutoArm/RoboTest/opensource_code/script/'
    file_name = ''
    script_name = ''
    temp_picture = 'picture'
    file_format = '.jpg'
    host_ip = '192.168.101.10'
    username = 'ubuntu'
    password = 'hiwonder'
    length = 15
    width = 7
    depth = 0.8

    phone_size = [20, 115, 578, 270]
    bottom_center_coordination = (0, 0)
    center_coordination = (0, 3.5)

    distance = 0
    last_coordination = (0, 0)
    last_last_coordination = (0, -1)

    is_replay = False
    # backend
    set_location(image_input_path, image_output_path, remote_path, local_path, control_base_path)
    set_phone_parameter(length, width, depth)
    set_file(file_name, file_format, script_base_path)
    set_ubuntu_connect(host_ip, username, password)

    # use multithreading to start back-end robotic arm related services
    robo_step = 1
    photo_step = 1
    TestRobot = TestRobot(image_input_path, image_output_path, remote_path, local_path)
    TestRobot.get_phone_parameter(length, width, depth)
    t1 = threading.Thread(target=robotest)
    t1.start()

    app.run(host='127.0.0.1', port=5000)
