#!/usr/bin/env python3

import rospy
import time
import sys
import board
import busio
from sensor_msgs.msg import MagneticField,Imu
from std_msgs.msg import Float64
import qwiic_icm20948

def icm20948_node():

    # Initialize ROS node
	#IMU topic name Changed 
    raw_pub = rospy.Publisher('imu/data', Imu, queue_size=10) 
    mag_pub = rospy.Publisher('imu/mag', MagneticField, queue_size=10)
    rospy.init_node('icm20948')

    rate = rospy.Rate(100)
    rospy.loginfo(rospy.get_caller_id() + "  icm20948 node launched.")

    IMU = qwiic_icm20948.QwiicIcm20948()

    while IMU.connected == False:
        message = "The Qwiic ICM20948 device isn't connected to the system. Please check your connection"
        rospy.loginfo(message)

    IMU.begin()    

    while not rospy.is_shutdown():
        if IMU.dataReady():
            IMU.getAgmt()
            raw_msg = Imu()
            raw_msg.header.stamp = rospy.Time.now()
            raw_msg.header.frame_id="imu_link"
	    	            
            raw_msg.orientation.w = 0
            raw_msg.orientation.x = 0
            raw_msg.orientation.y = 0
            raw_msg.orientation.z = 0
                
            raw_msg.linear_acceleration.x = IMU.axRaw
            raw_msg.linear_acceleration.y = IMU.ayRaw
            raw_msg.linear_acceleration.z = IMU.azRaw
                
            raw_msg.angular_velocity.x = IMU.gxRaw
            raw_msg.angular_velocity.y = IMU.gyRaw
            raw_msg.angular_velocity.z = IMU.gzRaw
                
            raw_msg.orientation_covariance[0] = -1
            raw_msg.linear_acceleration_covariance[0] = -1
            raw_msg.angular_velocity_covariance[0] = -1
                
            raw_pub.publish(raw_msg)
                
            mag_msg = MagneticField()
            mag_msg.header.stamp = rospy.Time.now()
            mag_msg.magnetic_field.x = IMU.mxRaw
            mag_msg.magnetic_field.y = IMU.myRaw
            mag_msg.magnetic_field.z = IMU.mzRaw
            mag_msg.magnetic_field_covariance[0] = -1
            mag_pub.publish(mag_msg)

        rate.sleep()   
    
    rospy.loginfo(rospy.get_caller_id() + "  icm20948 node finished")

if __name__ == '__main__':
    try:
        icm20948_node()
    except rospy.ROSInterruptException:
        rospy.loginfo(rospy.get_caller_id() + "  icm20948 node exited with exception.")
