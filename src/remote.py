#!/usr/bin/env python2
import rospy
import math
import RPi.GPIO as GPIO
from time import sleep
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
import numpy as np

rospy.init_node('receiver', anonymous=True)


GPIO.setmode(GPIO.BCM)
 
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
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

# def odom_callback(odom_data):
#     global odom_data
#     odom_data = odom_data

def move(x_setvel,y_setvel):


    if x_setvel >0:

        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH) 
        rospy.loginfo("Going Forward")
        GPIO.output(Motor2E,GPIO.LOW) 
        GPIO.output(Motor1E,GPIO.LOW)
        r = rospy.Rate(10)
        r.sleep()
        # GPIO.cleanup()
    elif x_setvel < 0:
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)             
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
        rospy.loginfo("Going Backward")   

        GPIO.output(Motor2E,GPIO.LOW) 
        GPIO.output(Motor1E,GPIO.LOW)
        # GPIO.cleanup()
        r = rospy.Rate(10)
        r.sleep()


    if y_setvel > 0 :

        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        rospy.loginfo("Going right")
        GPIO.output(Motor1E,GPIO.LOW)
        r = rospy.Rate(10)
        r.sleep()
    elif y_setvel < 0 :
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)        
        rospy.loginfo("Going Left") 
        GPIO.output(Motor2E,GPIO.LOW)
        r = rospy.Rate(10)
        r.sleep()

if __name__ == '__main__':
    while True: 
        goal = Twist()
        goal = rospy.wait_for_message("vel",Twist)
        move(goal.linear.x,goal.angular.z)
    
else: 
    rospy.loginfo("Error")
 
