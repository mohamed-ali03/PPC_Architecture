#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from ppc_interfaces.srv import MissionSRV
from ppc_interfaces.msg import MissionMSG
import time


class MissionServerNode(Node):
    def __init__(self):
        super().__init__("mission_service")
        self.mission_pub = self.create_publisher(MissionMSG,"mission",10)
        self.mission_servic = self.create_service(MissionSRV,"start_mission",self.mission_service_callback)
        self.time = self.create_timer(1.0,self.publish_mission)
        self.mission_msg = MissionMSG()

    def mission_service_callback(self,requst,response):
        self.mission_msg.mission_name= requst.mission_name
        if self.mission_msg.mission_name == "GoTo":
            self.mission_msg.target_pose.position.x = requst.target_pose.position.x
            self.mission_msg.target_pose.position.y = requst.target_pose.position.y
            response.accepted = True
            self.get_logger().info(f"Go to ({self.mission_msg.target_pose.position.x},{self.mission_msg.target_pose.position.y}).")
        elif self.mission_msg.mission_name == "Stop":
            response.accepted = True
            self.get_logger().info("Go to idle mode")
        else :
            self.get_logger().info("Not accepted")
            response.accepted = False
        
        return response
    
    def publish_mission(self):
        self.mission_pub.publish(self.mission_msg)


def main(argv=None):
    rclpy.init()
    node = MissionServerNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()