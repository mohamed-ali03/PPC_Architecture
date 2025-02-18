#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from rclpy.action import ActionServer
from ppc_interfaces.action import Navigate
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Point
from nav_msgs.msg import Path
import math 


class NavigateStateNode(Node):
    def __init__(self):
        super().__init__("Navigate_State_Node")
        self.state_sub= ActionServer(
            self,
            Navigate,
            "navigate",
            execute_callback=self.navigate)
        self.sub_current_pose = self.create_subscription(Odometry,"/odom",self.Current_Pose,10)
        self.vel_pub = self.create_publisher(Twist,"/cmd_vel",10)
        self.current_pose = Point()
        self.path = Path()

    def Current_Pose(self,msg:Odometry):
        self.current_pose.x = msg.pose.pose.position.x
        self.current_pose.y = msg.pose.pose.position.y

    def navigate(self,goal_handle):
        self.get_logger().info('Executing goal...')
        
        # Simulate navigation (replace with actual logic)
        
        self.path = goal_handle.path
        feedback_msg = Navigate.Feedback()
        result_msg = Navigate.Result()

        poses = 2
        for i in range(1,poses):
            dy = self.path.poses[i-1].pose.position.y - self.path.poses[i].pose.position.y
            dx = self.path.poses[i-1].pose.position.x - self.path.poses[i].pose.position.x
            angle_radian = math.atan2(dy,dx)
            angular_speed = 1.0
            rotation_time = angle_radian/angular_speed

            distance = math.sqrt((dx)**2 + (dy)**2)
            linear_speed = math.sqrt(2)
            move_time = linear_speed/distance

            self.change_angle(rotation_time)
            self.move_distance(move_time)

            feedback_msg.distance_to_goal = distance
            feedback_msg.speed = linear_speed
            goal_handle.publish_feedback(feedback_msg)


        goal_handle.succeed()
        result_msg.success = True
        return result_msg


    def change_angle(self,period):
        angular_speed = Twist()
        angular_speed.linear.x = 0.0
        angular_speed.linear.y = 0.0
        angular_speed.angular.z = 1.0
        self.vel_pub.publish(angular_speed)
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < period:
            pass 
        angular_speed.linear.x = 0.0
        angular_speed.linear.y = 0.0
        angular_speed.angular.z = 0.0
        self.vel_pub.publish(angular_speed)
        
    def move_distance(self,moving_time):
        linear_speed = Twist()
        linear_speed.linear.x = 1.0
        linear_speed.linear.y = 1.0
        linear_speed.angular.z = 0.0
        self.vel_pub.publish(linear_speed)
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < moving_time:
            pass 
        linear_speed.linear.x = 0.0
        linear_speed.linear.y = 0.0
        linear_speed.angular.z = 0.0
        self.vel_pub.publish(linear_speed)
    
        


def main(argv=None):
    rclpy.init()
    node = NavigateStateNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()