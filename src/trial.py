import rospy
import math
from time import sleep
from nav_msgs.msg import Odometry
import tf_conversions 
from geometry_msgs.msg import Quaternion
import numpy as np

rospy.init_node('motion_planning', anonymous=True)
odom_data = Odometry()

odom_data = rospy.wait_for_message("ar_pose_marker",Odometry)

print(odom_data.header)
 
