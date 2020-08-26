import rospy
import math
import RPi.GPIO as GPIO
from time import sleep
from nav_msgs.msg import Odometry
import tf_conversions 
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Point
import numpy as np

rospy.init_node('motion_planning', anonymous=True)
odom_data = Odometry()

GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 17
Motor2B = 19
Motor2E = 23

ed = 0.1
ea = 0.1

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

# def odom_callback(odom_data):
#     global odom_data
#     odom_data = odom_data

def move(x_setpoint,y_setpoint):
    global odom_data
    reached = 0
    while reached != 1:

        odom_data = rospy.wait_for_message("/camera/odom/sample", Odometry)
        # print(odom_data)

        quaternion = Quaternion()
        quaternion = [odom_data.pose.pose.orientation.x,odom_data.pose.pose.orientation.y,odom_data.pose.pose.orientation.z,odom_data.pose.pose.orientation.w]

        roll, pitch, yaw = tf_conversions.transformations.euler_from_quaternion(quaternion)

        if y_setpoint - odom_data.pose.pose.position.y !=0:
            theta = math.atan((x_setpoint - odom_data.pose.pose.position.x)/(y_setpoint - odom_data.pose.pose.position.y))
        else:
            theta = 1.57

        if x_setpoint - odom_data.pose.pose.position.x > 0:
            if theta <0 :
                theta = math.pi - theta
        
            while yaw - ea < theta < yaw + ea:

                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                GPIO.output(Motor1E,GPIO.HIGH)
                rospy.loginfo("Going right")
            GPIO.output(Motor1E,GPIO.LOW)
    
        elif x_setpoint - odom_data.pose.pose.position.x < 0 :
            if theta < 0:
                theta = -theta
            else:
                theta = math.pi - theta
        
            while yaw - ea < theta < yaw + ea:

                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                GPIO.output(Motor2E,GPIO.HIGH)        
                rospy.loginfo("Going Left") 
            GPIO.output(Motor2E,GPIO.LOW)

        while  -ed < y_setpoint - odom_data.pose.pose.position.y < ed :
            if y_setpoint - odom_data.pose.pose.position.y > 0 : 
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                GPIO.output(Motor1E,GPIO.HIGH)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                GPIO.output(Motor2E,GPIO.HIGH) 
                rospy.loginfo("Going Forward")
            else : 
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                GPIO.output(Motor1E,GPIO.HIGH)             
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                GPIO.output(Motor2E,GPIO.HIGH)
                rospy.loginfo("Going Backward")   

        GPIO.output(Motor2E,GPIO.LOW) 
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.cleanup()
        if  -ed< odom_data.pose.pose.orientation.x - x_setpoint <ed and -ed< odom_data.pose.pose.orientation.y - y_setpoint <ed :
            reached = 1

if __name__ == '__main__':
    while True: 
        goal = Point()
        goal = rospy.wait_for_message("destination",Point)
        move(goal.x,goal.y)
    
else: 
    rospy.loginfo("Error")
 
