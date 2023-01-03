# ros-ngimu

## First step
	
### Give the permission to /ttyACM0
	
	sudo chmod 777 /dev/ttyACM0

## Run imu data

	roslaunch ros-ngimu run.launch
	rostopic echo /imu/data


## Run imu calibration

	rosrun imu_calib do_calib
	
	sudo cp imu_calib.yaml ~/.ros

## Run imu clibration data

	roslaunch ros-ngimu run_cal.launch
	
## Run rviz imu data

	roslaunch ros-ngimu run_rviz.launch
	
	
## apply imu accel data low pass filter 

	roslaunch ros-ngimu run_rviz.launch
	python src/ros-ngimu/src/draw_graph_low_pass.py
	
	
## run madgwick filter
	
	roslaunch ros-ngimu run_rviz.launch
	roslaunch imu_filter_madgwick imu_filter_madgwick.launch

## run xioTechnologies imu fution tool
	
	roslaunch ros-ngimu run_rviz.launch
	python src/Fusion-main/Python/test.py
