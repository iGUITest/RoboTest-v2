import sys

sys.path.append('ArmPi_PC_Software')

from BusServoControl import *
import time;
from kinematics import ik_transform

ik = ik_transform.ArmIK()


class Control(object):
    def __init__(self, depth):
        # initial coordinates (0,0.075,-0.01) meter
        self.x_dis = 0
        self.y_dis = 0.100
        self.z_dis = 0
        
        self.depth = depth
        self.up_dis = 0
        self.down_dis = -5.05 + depth

        # init robot location
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, -180)
        if target:
            print("init successfully!")
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)

    def reset(self):
        self.x_dis = 0
        self.y_dis = 0.100
        self.z_dis = 0

        # reset robot location
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, -180)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)

    def turn_right_left(self, left_right):
        self.x_dis = self.x_dis + left_right / 100
        if self.x_dis > 0.2:
            self.x_dis = 0.2
        if self.x_dis < -0.2:
            self.x_dis = -0.2
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, -180)
        if target:
            print("turn left/right successfully!")
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)

    def turn_forward_backward(self, forward_backward):
        self.y_dis = self.y_dis + forward_backward / 100
        if self.y_dis < 0.075:
            self.y_dis = 0.075
        if self.y_dis > 0.165:
            self.y_dis = 0.165
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, -180)
        if target:
            print("turn forward/backward successfully!")
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)
        time.sleep(2)

    def turn_up_down(self, up_down, speed):
        self.z_dis = self.z_dis + up_down / 100
        if self.z_dis > 0.04:
            self.z_dis = 0.04
        if self.z_dis < -0.08:
            self.z_dis = -0.08
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            print("turn up/down successfully!")
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], speed)
            setBusServoPulse(4, servo_data['servo4'], speed)
            setBusServoPulse(5, servo_data['servo5'], speed)
            return target

    def click(self, x, y):

        # move arm
        self.x_dis = self.x_dis + x / 100
        self.y_dis = self.y_dis + y / 100
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)
        time.sleep(1)

        # click
        self.turn_up_down(self.down_dis, 300)
        time.sleep(0.4)

        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 300)
            setBusServoPulse(4, servo_data['servo4'], 300)
            setBusServoPulse(5, servo_data['servo5'], 300)
            setBusServoPulse(6, servo_data['servo6'], 300)

        time.sleep(0.5)

        print("click successfully!")
        # reset arm
        self.reset()

    def long_click(self, x, y, t):

        # move arm
        self.x_dis = self.x_dis + x / 100
        self.y_dis = self.y_dis + y / 100
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)
        time.sleep(1)

        # click
        self.turn_up_down(self.down_dis, 300)
        time.sleep(t)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 300)
            setBusServoPulse(4, servo_data['servo4'], 300)
            setBusServoPulse(5, servo_data['servo5'], 300)
        time.sleep(0.5)

        print("long click successfully!")

        # reset arm
        self.reset()

    def double_click(self, x, y):

        # move arm
        self.x_dis = self.x_dis + x / 100
        self.y_dis = self.y_dis + y / 100
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)
        time.sleep(1)

        # click
        target_down = self.turn_up_down(self.down_dis, 300)
        time.sleep(0.4)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 300)
            setBusServoPulse(4, servo_data['servo4'], 300)
            setBusServoPulse(5, servo_data['servo5'], 300)
        time.sleep(0.4)

        if target_down:
            servo_data = target_down[1]
            setBusServoPulse(3, servo_data['servo3'], 300)
            setBusServoPulse(4, servo_data['servo4'], 300)
            setBusServoPulse(5, servo_data['servo5'], 300)
        time.sleep(0.4)

        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 300)
            setBusServoPulse(4, servo_data['servo4'], 300)
            setBusServoPulse(5, servo_data['servo5'], 300)
        time.sleep(0.4)

        print("double click successfully!")
        # reset arm
        self.reset()

    def slide(self, x1, y1, x2, y2):

        # move arm
        self.x_dis = self.x_dis + x1 / 100
        self.y_dis = self.y_dis + y1 / 100
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)
        time.sleep(1)

        target_down = self.turn_up_down(self.down_dis, 300)
        time.sleep(0.4)

        self.x_dis = 0 + x2 / 100
        self.y_dis = 0.075 + y2 / 100
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 200)
            setBusServoPulse(4, servo_data['servo4'], 200)
            setBusServoPulse(5, servo_data['servo5'], 200)
            setBusServoPulse(6, servo_data['servo6'], 200)
        time.sleep(0.6)

        self.turn_up_down(-self.down_dis, 300)
        time.sleep(0.5)

        print("slide successfully!")
        # reset arm
        self.reset()

    def scroll(self, x, y, dis):

        # move arm
        self.x_dis = self.x_dis + x / 100
        self.y_dis = self.y_dis + y / 100
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            servo_data = target[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)
        time.sleep(1)

        # click
        self.turn_up_down(self.down_dis, 300)
        time.sleep(1)

        self.x_dis = self.x_dis + dis / 100
        target_scroll = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target_scroll:
            servo_data = target_scroll[1]
            setBusServoPulse(3, servo_data['servo3'], 500)
            setBusServoPulse(4, servo_data['servo4'], 500)
            setBusServoPulse(5, servo_data['servo5'], 500)
            setBusServoPulse(6, servo_data['servo6'], 500)
        time.sleep(1)

        self.turn_up_down(self.up_dis, 300)
        time.sleep(0.5)

        print("scroll successfully!")

        # reset arm
        self.reset()


#control = Control(0.813)
#control.turn_up_down(-4.7,300)
#
#control.slide(-4,1,5,1)
# control.turn_up_down(4,300)
'''control.scroll(2,2,4)
time.sleep(1)
control.slide(1,1,4,4)
time.sleep(1)
control.double_click(-3,3)
time.sleep(1)
control.click(5,2)
time.sleep(1)
control.long_click(4,2,3)'''

# control.turn_up_down(2)
# time.sleep(1)
# control.turn_right_left(-750)
# time.sleep(2)
# control.turn_forward_backward(5)
# time.sleep(1)
# control.turn_forward_backward(900)

