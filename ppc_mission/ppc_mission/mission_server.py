#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from ppc_interfaces.srv import MissionSRV
from ppc_interfaces.msg import MissionMSG


class MissionServerNode(Node):
    def __init__(self):
        super().__init__("mission_service")
        self.mission_pub = self.create_publisher(MissionMSG,"mission",10)
        self.mission_servic = self.create_service(MissionSRV,"start_mission",self.mission_service_callback)
        

    def mission_service_callback(self,requst,response):
        mission_msg = MissionMSG()
        mission_msg.mission_name= requst.mission_name
        if mission_msg.mission_name == "GoTo":
            mission_msg.x_pose = requst.x_pose
            mission_msg.y_pose = requst.y_pose
            self.get_logger().info(f"Go to ({mission_msg.x_pose},{mission_msg.y_pose}).")
            response.accepted = True
            self.mission_pub.publish(mission_msg)
        elif mission_msg.mission_name == "Stop":
            self.get_logger().info("Go to idle mode")
            response.accepted = True
            self.mission_pub.publish(mission_msg)
        else :
            self.get_logger().info("Not accepted")
            response.accepted = False
        
        return response


def main(argv=None):
    rclpy.init()
    node = MissionServerNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()