make:
	source devel/setup.bash
export:
	export TURTLEBOT3_MODEL=waffle
empty:
	roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
key:
	python3 ~/simu/src/linear/linear_ramp_controller.py
slam:
	roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping
navigation:
	roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml
