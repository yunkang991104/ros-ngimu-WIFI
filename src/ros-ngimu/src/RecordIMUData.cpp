#include <ros/ros.h>
#include <sensor_msgs/Imu.h>
#include <fstream>
#include <unistd.h>
#include <ctime>
#include <string>
#include <chrono>

std::ofstream csv_file;
using std::string;
using std::to_string;

void imuCallback(const sensor_msgs::Imu::ConstPtr &msg)
{
    // Write the IMU data to the CSV file
    csv_file << msg->linear_acceleration.x << ","
             << msg->linear_acceleration.y << ","
             << msg->linear_acceleration.z << ","
             << msg->angular_velocity.x << ","
             << msg->angular_velocity.y << ","
             << msg->angular_velocity.z << std::endl;
    std::cout << msg->linear_acceleration.x << ","
              << msg->linear_acceleration.y << ","
              << msg->linear_acceleration.z << ","
              << msg->angular_velocity.x << ","
              << msg->angular_velocity.y << ","
              << msg->angular_velocity.z << std::endl;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "record_imu");
    ros::NodeHandle nh;

    auto now = std::chrono::system_clock::now();
    std::time_t now_time = std::chrono::system_clock::to_time_t(now);

    std::tm *time_info = std::localtime(&now_time);
    int hour = time_info->tm_hour;
    int minute = time_info->tm_min;
    int second = time_info->tm_sec;

    int frequency = 400;

    string filename = "IMUData_";

    filename += to_string(hour) + "_" + to_string(minute) + "_" + to_string(second) + "_" + to_string(frequency) + "Hz.csv";

    // Open the CSV file for writing
    csv_file.open(filename.c_str());
    csv_file << "linear_acceleration.x,linear_acceleration.y,linear_acceleration.z,angular_velocity.x,angular_velocity.y,angular_velocity.z," << std::endl;
    std::cout << "linear_acceleration.x,linear_acceleration.y,linear_acceleration.z,angular_velocity.x,angular_velocity.y,angular_velocity.z," << std::endl;
    // Subscribe to the IMU topic
    ros::Subscriber imu_sub = nh.subscribe("imu/data_raw", frequency, imuCallback);

    ros::spin();

    // Close the CSV file
    csv_file.close();

    return 0;
}
