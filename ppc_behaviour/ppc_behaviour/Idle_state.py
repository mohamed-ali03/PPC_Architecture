#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class IdleStateNode(Node):
    def __init__(self):
        super().__init__("Idle_State_Node")
        self.state_sub= self.create_subscription(String,"state",self.state_callback,10)
        self.Stop_Rover = self.create_publisher(Twist,"/cmd_vel",10)

    def state_callback(self,msg:String):
        vel = Twist()
        vel.linear.x = 0.0
        vel.linear.y = 0.0 
        vel.linear.z = 0.0
        vel.angular.x = 0.0
        vel.angular.y = 0.0 
        vel.angular.z = 0.0
        self.Stop_Rover.publish(vel)
            



def main(argv=None):
    rclpy.init()
    node = IdleStateNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()