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
    x_meas = x_acc_list[-1]

    x_esti = lpf.low_pass_filter(x_meas, x_esti)

    x_esti_list.append(x_esti)

    # print(x_acc_list)
    # print(y_acc_list)
    # print(z_acc_list)

def animate(i):

    if len(x_esti_list):
        plt.cla()
        plt.plot(x_index[int(len(x_acc_list)/3):len(x_acc_list)], x_acc_list[int(len(x_acc_list)/3):len(x_acc_list)])
        plt.plot(x_index[int(len(x_esti_list)/3):len(x_esti_list)], x_esti_list[int(len(x_esti_list)/3):len(x_esti_list)])
        # plt.plot(x_index[:len(x_esti_list)], x_esti_list[:len(x_esti_list)])



if __name__ == "__main__":
    rospy.init_node('Imu_read', anonymous=True)
    imu_sub = rospy.Subscriber('/imu/data', Imu, Imucallback)

    ani = FuncAnimation(plt.gcf(), animate, interval = 40)
 
    plt.tight_layout()
    plt.show()
    rospy.spin()