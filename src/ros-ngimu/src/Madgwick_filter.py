from ahrs.filters import Madgwick

import math
import rospy
from sensor_msgs.msg import Imu, MagneticField
from geometry_msgs.msg import Vector3

from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

import time

# x_gyr_list = []
# y_gyr_list = []
# z_gyr_list = []

# x_acc_list = []
# y_acc_list = []
# z_acc_list = []

# x_mag_list = []
# y_mag_list = []
# z_mag_list = []



gyro_data = []
acc_data = []
mag_data = []

quaternion_data = []

def qua2eular(x,y,z,w):

    q_x = x
    q_y = y
    q_z = z
    q_w = w

    t0 = +2.0 * (q_w * q_x + q_y * q_z)
    t1 = +1.0 - 2.0 * (q_x * q_x + q_y * q_y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (q_w * q_y - q_z * q_x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (q_w * q_z + q_x * q_y)
    t4 = +1.0 - 2.0 * (q_y * q_y + q_z * q_z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z # in radians



def Imucallback(msg):
    global acc_data, gyro_data, quaternion_data
    # x_gyr_list.append(msg.angular_velocity.x)
    # y_gyr_list.append(msg.angular_velocity.y)
    # z_gyr_list.append(msg.angular_velocity.z)

    # x_acc_list.append(msg.linear_acceleration.x)
    # y_acc_list.append(msg.linear_acceleration.y)
    # z_acc_list.append(msg.linear_acceleration.z)

    gyro_data = np.array([msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z])
    acc_data = np.array([msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z])
    quaternion_data = np.array([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])

def Imu_mag_callback(msg):
    global mag_data
    # x_mag_list.append(msg.magnetic_field.x)
    # y_mag_list.append(msg.magnetic_field.y)
    # z_mag_list.append(msg.magnetic_field.z)

    mag_data = np.array([msg.magnetic_field.x, msg.magnetic_field.y, msg.magnetic_field.z])
    
class Madgwich_Filter():

    def __init__(self, gyro_data, acc_data, mag_data, quaternion_data):

        self.Q = quaternion_data

        self.gyro_data = gyro_data
        self.acc_data = acc_data
        self.mag_data = mag_data

        self.madgwick = Madgwick(updateMARG = 400, gain=0.05)

    # if len(gyro_data) and len(acc_data) and len(mag_data):
        # madgwick = Madgwick(gyr=gyro_data, acc=acc_data, mag = mag_data, gain=0.01)
    
    
    def update(self, gyro_data, acc_data, mag_data, quaternion_data):

        self.Q = quaternion_data

        # print("gyro_data", gyro_data)
        # print("acc_data", acc_data)
        # print("mag_data", mag_data)


        self.Q = self.madgwick.updateMARG(self.Q, gyr=gyro_data, acc=acc_data, mag = mag_data)



mf_flag = 0

if __name__ == "__main__":

    rospy.init_node('Imu_read', anonymous=True)

    rate = rospy.Rate(400)
    
    imu_sub = rospy.Subscriber('/imu/low_pass', Imu, Imucallback)
    imu_mag_sub = rospy.Subscriber('/imu/mag', MagneticField, Imu_mag_callback)
    
    time.sleep(1)

    if len(gyro_data) and len(acc_data) and len(mag_data) and mf_flag == 0:
        mf = Madgwich_Filter(gyro_data, acc_data, mag_data, quaternion_data)
        mf_flag = 1
    if mf_flag == 1:
        while 1:

                t0 = time.time()
                mf.update(gyro_data, acc_data, mag_data, quaternion_data)
                print(mf.Q)
                # roll, pitch, yaw = qua2eular(mf.Q[0],mf.Q[1],mf.Q[2],mf.Q[3])
                # print(np.rad2deg(roll), np.rad2deg(pitch), np.rad2deg(yaw))
                rate.sleep()
                # print(1/(time.time()-t0))
    rospy.spin()
