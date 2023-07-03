# ros-ngimu

## First step
	
### Connect your NGIMU Wi-Fi
	
	Connect you your NGIMU using your ubuntu => select network.

## OPEN BASHRC

	gedit ~/.bashrc
	


## Paste this to bashrc somewhere.Don't forget to comment these code. # export ROS_MASTER_URI=http://localhost:11311 # export ROS_IP=localhost

	# Using NGIMU
       export ROS_MASTER_URI=http://192.168.1.2:11311
       export ROS_HOSTNAME=192.168.1.2

## Run imu 

	roslaunch ros-ngimu run.launch
	
## Run rviz imu

	roslaunch ros-ngimu run_rviz.launch
	
