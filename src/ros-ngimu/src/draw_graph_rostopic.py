import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3

from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import low_pass_filter as lpf

x_acc_list = []
y_acc_list = []
z_acc_list = []

x_acc_list_2 = []
y_acc_list_2 = []
z_acc_list_2 = []


index = count()

x_index = []
x_esti_list = []
x_esti = 0


def Imucallback(msg):
    global x_esti

    x_acc_list.append(msg.linear_acceleration.x)
    y_acc_list.append(msg.linear_acceleration.y)
    z_acc_list.append(msg.linear_acceleration.z)
    x_index.append(next(index))

    # print(x_acc_list)
    # print(y_acc_list)
    # print(z_acc_list)


def Imu_low_pass_callback(msg):

    x_acc_list_2.append(msg.linear_acceleration.x)
    y_acc_list_2.append(msg.linear_acceleration.y)
    z_acc_list_2.append(msg.linear_acceleration.z)


def animate(i):

    if len(x_esti_list):
        plt.cla()
        plt.plot(x_index[int(len(x_acc_list)/3):len(x_acc_list)], x_acc_list[int(len(x_acc_list)/3):len(x_acc_list)])
        plt.plot(x_index[int(len(x_acc_list_2)/3):len(x_acc_list_2)], x_acc_list_2[int(len(x_acc_list_2)/3):len(x_acc_list_2)])
        # plt.plot(x_index[:len(x_esti_list)], x_esti_list[:len(x_esti_list)])



if __name__ == "__main__":
    rospy.init_node('Imu_read', anonymous=True)
    imu_sub = rospy.Subscriber('/imu/data_raw', Imu, Imucallback)
    imu_low_pass_sub = rospy.Subscriber('/imu/low_pass', Imu, Imu_low_pass_callback)


    ani = FuncAnimation(plt.gcf(), animate, interval = 40)
 
    plt.tight_layout()
    plt.show()
    rospy.spin()