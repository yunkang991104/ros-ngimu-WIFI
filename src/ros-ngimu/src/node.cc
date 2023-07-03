#include <ros/ros.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/MagneticField.h>
#include <geometry_msgs/PoseStamped.h>
#include <tf/transform_broadcaster.h>
#include <thread>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "NgimuReceive.h"

#define NGIMU_IP "192.168.1.2"
#define NGIMU_PORT 8001
#define BUFFER_SIZE 1024

ros::Publisher imuPub;
ros::Publisher magPub;
ros::Publisher posePub;
sensor_msgs::Imu imuData;
sensor_msgs::MagneticField mag_data;
geometry_msgs::PoseStamped pose;
tf::TransformBroadcaster *transformBroadcaster;

void ngimuSensorsCallback(const NgimuSensors ngimuSensors) {
    // Set time
    ros::Time current_time = ros::Time::now();
    imuData.header.stamp = current_time;
    mag_data.header.stamp = current_time;
    imuData.header.frame_id = "imu_link";
    mag_data.header.frame_id = "imu_link";

    // Accelerometer
    imuData.linear_acceleration.x = ngimuSensors.accelerometerX * 9.8;
    imuData.linear_acceleration.y = ngimuSensors.accelerometerY * 9.8;
    imuData.linear_acceleration.z = ngimuSensors.accelerometerZ * 9.8;

    // Gyroscope
    imuData.angular_velocity.x = ngimuSensors.gyroscopeX * 0.0174533;
    imuData.angular_velocity.y = ngimuSensors.gyroscopeY * 0.0174533;
    imuData.angular_velocity.z = ngimuSensors.gyroscopeZ * 0.0174533;

    // Magnetometer
    mag_data.magnetic_field.x = ngimuSensors.magnetometerX * 1000;
    mag_data.magnetic_field.y = ngimuSensors.magnetometerY * 1000;
    mag_data.magnetic_field.z = ngimuSensors.magnetometerZ * 1000;

    // Publish the data
    imuPub.publish(imuData);
    magPub.publish(mag_data);

    // Update pose message header
    pose.header.stamp = current_time;
    pose.header.frame_id = "odom";

    // Broadcast transform
    tf::Transform transform;
    transform.setOrigin(tf::Vector3(pose.pose.position.x, pose.pose.position.y, 0.0));
    transform.setRotation(tf::Quaternion(imuData.orientation.x, imuData.orientation.y, imuData.orientation.z, imuData.orientation.w));
    transformBroadcaster->sendTransform(tf::StampedTransform(transform, current_time, "odom", "base_link"));
}

void ngimuQuaternionCallback(const NgimuQuaternion ngimuQuaternion) {
    // Set time
    imuData.header.stamp = ros::Time::now();
    imuData.header.frame_id = "imu_link";

    // Orientation (Quaternion)
    imuData.orientation.x = ngimuQuaternion.x;
    imuData.orientation.y = ngimuQuaternion.y;
    imuData.orientation.z = ngimuQuaternion.z;
    imuData.orientation.w= ngimuQuaternion.w;

    // Publish the data
    imuPub.publish(imuData);
}

void receiveImu() {
    int sockfd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in servaddr;

    // Creating socket file descriptor
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));

    // Filling server information
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(NGIMU_PORT);
    servaddr.sin_addr.s_addr = inet_addr(NGIMU_IP);

    // Bind the socket with the server address
    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    int n;
    socklen_t len = sizeof(servaddr);
    while (ros::ok()) {
        n = recvfrom(sockfd, (char *)buffer, BUFFER_SIZE, MSG_WAITALL, (struct sockaddr *) &servaddr, &len);
        NgimuReceiveProcessUdpPacket(buffer, n);
    }
}

int main(int argc,char **argv) {
    ros::init(argc, argv, "ngimu");
    ros::NodeHandle n;

    imuPub = n.advertise<sensor_msgs::Imu>("/imu/data_raw", 400);
    magPub = n.advertise<sensor_msgs::MagneticField>("/imu/mag", 400);
    posePub = n.advertise<geometry_msgs::PoseStamped>("/imu/pose", 400);

    transformBroadcaster = new tf::TransformBroadcaster();

    NgimuReceiveInitialise();
    NgimuReceiveSetSensorsCallback(ngimuSensorsCallback);
    NgimuReceiveSetQuaternionCallback(ngimuQuaternionCallback);

    std::thread th1(receiveImu);
    th1.detach();

    ros::spin();

    delete transformBroadcaster;
    return 0;
}
