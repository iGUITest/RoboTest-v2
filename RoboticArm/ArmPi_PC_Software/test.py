from BusServoControl import *
import time;
from kinematics import ik_transform

ik = ik_transform.ArmIK()

class Control(object):
    def __init__(self):
        self.x_dis = 0
        self.y_dis = 0.075
        self.z_dis = -0.01

        #init location
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, -180);
        if target:
            servo_data = target[1];
            setBusServoPulse(1, 800, 500);
            setBusServoPulse(3, servo_data['servo3'], 500);
            setBusServoPulse(4, servo_data['servo4'], 500);
            setBusServoPulse(5, servo_data['servo5'], 500);
            setBusServoPulse(6, servo_data['servo6'], 500);

        time.sleep(2)



    def turn_right_left(self,left_right):
        self.x_dis = self.x_dis + left_right / 10000
        if self.x_dis > 0.2:
            self.x_dis = 0.2
        if self.x_dis < -0.2:
            self.x_dis = -0.2
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, -180);
        if target:
            print("turn left/right successfully!")
            servo_data = target[1];
            setBusServoPulse(3, servo_data['servo3'], 500);
            setBusServoPulse(4, servo_data['servo4'], 500);
            setBusServoPulse(5, servo_data['servo5'], 500);
            setBusServoPulse(6, servo_data['servo6'], 500);


    def turn_forward_backward(self, forward_backward):
        self.y_dis = self.y_dis + forward_backward/10000
        if self.y_dis < 0.075:
            self.y_dis = 0.075
        if self.y_dis > 0.165:
            self.y_dis = 0.165
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, -180);
        if target:
            print("turn forward/backward successfully!")
            servo_data = target[1];
            setBusServoPulse(3, servo_data['servo3'], 500);
            setBusServoPulse(4, servo_data['servo4'], 500);
            setBusServoPulse(5, servo_data['servo5'], 500);
            setBusServoPulse(6, servo_data['servo6'], 500);
        time.sleep(2)

    def turn_up_down(self, up_down):
        self.z_dis = self.z_dis + up_down/10000
        if self.z_dis > 0:
            self.z_dis = 0
        if self.z_dis < -0.08:
            self.z_dis = -0.08
        target = ik.setPitchRanges((self.x_dis, self.y_dis, self.z_dis), -180, -180, 0)
        if target:
            print("turn up/down successfully!")
            servo_data = target[1];
            setBusServoPulse(3, servo_data['servo3'], 500);
            setBusServoPulse(4, servo_data['servo4'], 500);
            setBusServoPulse(5, servo_data['servo5'], 500);
        time.sleep(2)


control = Control()

#control.turn_up_down(200)
#time.sleep(1)
#control.turn_right_left(-750)
#time.sleep(2)
control.turn_forward_backward(500)
#time.sleep(1)
#control.turn_forward_backward(900)

