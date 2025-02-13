#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from std_msgs.msg import String


class IdleStateNode(Node):
    def __init__(self):
        super().__init__("IdleStateNode")
        self.state_sub= self.create_subscription(String,"state",self.state_callback,10)

    def state_callback(self,msg:String):
        if msg.data == "idle":
            self.get_logger().info("idle")
            



def main(argv=None):
    rclpy.init()
    node = IdleStateNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()