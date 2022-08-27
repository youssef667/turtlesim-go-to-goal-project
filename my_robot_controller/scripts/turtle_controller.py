#!/usr/bin/env python3
#this node is a puplisher to velocity topis and a subscriber to pose topic which makes a closed loop#
import rospy
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import String

#to get the constants from the user#
k_linear = float(input("\nEnter the constant for the linear velocity: \n"))
k_angular = float(input("Enter the constant for the angular velocity: \n"))
#to get the constants from .yaml file#
rospy.set_param("/linear_constant", k_linear)
rospy.set_param("/angular_constant", k_angular)
goal_pose = Pose()
vel_msg = Twist()
 #take the final distnation from the user#
goal_pose.x = float(input("Enter x-cordinate of the goal: "))
goal_pose.y = float(input("Enter y-cordinate of the goal: "))
   #take the final distnation from .yaml file#
#goal_pose.x = rospy.get_param("/x_coordinate")
#goal_pose.y = rospy.get_param("/y_coordinate")

def pose_callback(pose:Pose):

   cmd =Twist()
    
   pose.x =round(pose.x,4)
   pose.y =round(pose.y,4)
   distance_to_move= abs(math.sqrt(((goal_pose.x-pose.x)**2) + ((goal_pose.x-pose.x)**2)))
   
   desired_angle = (-pose.theta) + math.atan2(goal_pose.y-pose.y , goal_pose.x-pose.x)
   
   if distance_to_move>= 0.11:
     cmd.linear.x=k_linear * distance_to_move
     cmd.angular.z=k_angular * desired_angle
     pup.publish(cmd)
   else:  
       cmd.linear.x=0
       cmd.linear.y=0
       cmd.linear.z=0
       cmd.angular.z=0
       cmd.angular.y=0
       cmd.angular.x=0
       pup.publish(cmd) 
       print("Succesfully Reached the goal (",  goal_pose.x, ",", goal_pose.y, ")")   



if __name__=='__main__':

    rospy.init_node("turtle_controller")
    pup=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    sub = rospy.Subscriber("/turtle1/pose",Pose,callback=pose_callback)
    rospy.loginfo("node_has_been_started")
  
rospy.spin()