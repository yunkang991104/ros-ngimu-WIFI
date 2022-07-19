import imufusion

import matplotlib.pyplot as pyplot
import numpy as np
import sys

import rospy
from sensor_msgs.msg import Imu, MagneticField

gyro_data = []
acc_data = []
mag_data = []

quaternion_data = []

def Imucallback(msg):
    global acc_data, gyro_data, quaternion_data
    # x_gyr_list.append(msg.angular_velocity.x)
    # y_gyr_list.append(msg.angular_velocity.y)
    # z_gyr_list.append(msg.angular_velocity.z)

    # x_acc_list.append(msg.linear_acceleration.x)
    # y_acc_list.append(msg.linear_acceleration.y)
    # z_acc_list.append(msg.linear_acceleration.z)

    gyro_data = np.array([msg.angular_velocity.x / 0.0174533, msg.angular_velocity.y / 0.0174533, msg.angular_velocity.z / 0.0174533])
    acc_data = np.array([msg.linear_acceleration.x / 9.8, msg.linear_acceleration.y / 9.8, msg.linear_acceleration.z / 9.8])
    quaternion_data = np.array([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])

def Imu_mag_callback(msg):
    global mag_data
    # x_mag_list.append(msg.magnetic_field.x)
    # y_mag_list.append(msg.magnetic_field.y)
    # z_mag_list.append(msg.magnetic_field.z)

    mag_data = np.array([msg.magnetic_field.x / 1000, msg.magnetic_field.y / 1000, msg.magnetic_field.z / 1000])

if __name__ == "__main__":

    rospy.init_node('Imu_read', anonymous=True)

    rate = rospy.Rate(400)
    
    imu_sub = rospy.Subscriber('/imu/data_raw', Imu, Imucallback)
    imu_mag_sub = rospy.Subscriber('/imu/mag', MagneticField, Imu_mag_callback)

    sample_rate = 400
    offset = imufusion.Offset(sample_rate)
    ahrs = imufusion.Ahrs()

    ahrs.settings = imufusion.Settings(0.5,  # gain
                                   10,  # acceleration rejection
                                   20,  # magnetic rejection
                                    500)  # rejection timeout = 4 seconds

    pub = rospy.Publisher('imu_ahrs', Imu, queue_size=10)

    msg = Imu()
    
    while not rospy.is_shutdown():

        if len(gyro_data) and len(acc_data) and len(mag_data):
            ahrs.update(gyro_data, acc_data, mag_data, 1 / 400)

            msg.header.stamp = rospy.get_rostime()

            msg.header.frame_id = "imu_link"

            msg.orientation.x = ahrs.quaternion.x
            msg.orientation.y = ahrs.quaternion.y
            msg.orientation.z = ahrs.quaternion.z
            msg.orientation.w = ahrs.quaternion.w


            msg.angular_velocity.x = gyro_data[0]
            msg.angular_velocity.y = gyro_data[1]
            msg.angular_velocity.z = gyro_data [2]

            msg.linear_acceleration.x = acc_data[0]
            msg.linear_acceleration.y = acc_data[1]
            msg.linear_acceleration.z = acc_data[2]

            pub.publish(msg)
            print(1)

            rate.sleep()

        pass

    rospy.spin()
