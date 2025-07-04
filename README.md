Trước hết em xin cảm ơn quý công ty đã giành thời gian quý báu để review em. Em rất trân trọng điều đó nhưng do quỹ thời gian của em khá hạn hẹp để có thể tiến hành xây mô model hoàn chỉnh nên em xin lấy mô hình có sẵn để thực hiện, và đồng thời trong file hahaa là model em đang thực hiện dang dỡ.

Để thực hiện điều khiển robot chạy 5m/s bằng nút nhắn thì em sử dụng model waffle tích hợp code python trong linear, code python này có tích hợp is_stoped nhầm hỗ trợ cho việc dừng nhanh với tốc độ chạy cao:
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
python3 ~/simu/src/linear/linear_ramp_controller.py

task3: 
slam:
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_stage_3.launch
roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping
rosrun map_server map_saver -f ~/map

navigate:
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml

**Ngoài ra model mà em tự phát triển nhưng đang dang dỡ:** 

navigate: 
roslaunch hahaa gazebo.launch navigation:=true

slam:
roslaunch hahaa gazebo.launch

Nếu sử dụng model navigate hahaa thì cần mở Rviz và add thủ công các topic.

 
