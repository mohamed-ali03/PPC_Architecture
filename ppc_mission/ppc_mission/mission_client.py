#!/usr/bin/env python
import sys
import rclpy 
from rclpy.node import Node
from functools import partial
from ppc_interfaces.srv import MissionSRV




class MissionClientNode(Node):
    def __init__(self):
        super().__init__("mission_client")
        self.mission_client = self.create_client(MissionSRV,"start_mission")
        while not self.mission_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available ,waiting again .....")
        

    def send_mission(self):
        self.requst = MissionSRV.Request()
        self.requst.mission_name = sys.argv[1]

        if self.requst.mission_name == "GoTo":
            self.requst.target_pose.position.x = float(sys.argv[2])
            self.requst.target_pose.position.y = float(sys.argv[3])

        future = self.mission_client.call_async(self.requst)
        future.add_done_callback(partial(self.callback_status))

    def callback_status(self, future):
        try:
            response = future.result()  
            if response.accepted:  
                self.get_logger().info("Service accepted the mission.")
            else:
                self.get_logger().info("Service rejected the mission.")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

def main(argv=None):
    rclpy.init()
    node = MissionClientNode()
    node.send_mission()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()