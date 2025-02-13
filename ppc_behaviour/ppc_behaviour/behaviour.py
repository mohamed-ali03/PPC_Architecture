#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from ppc_interfaces.msg import MissionMSG
from std_msgs.msg import String
from ppc_interfaces.srv import CreatePlanSRV
from nav_msgs.msg import Path


class BehaviourNode(Node):
    def __init__(self):
        super().__init__("BehaviourNode")
        self.mission_sub = self.create_subscription(MissionMSG,"mission",self.behaviour_callback,10)
        self.state_pub = self.create_publisher(String,"state",10)
        self.state = String()
        self.state.data = "idle state"
        self.state_pub.publish(self.state)

    def behaviour_callback(self,msg:MissionMSG):
        if msg.mission_name == "Stop":
            self.state.data = "idle state"
            self.state_pub.publish(self.state)
        elif msg.mission_name == "GoTo":
            # create plan
            self.state.data = "create plan state"
            self.state_pub.publish(self.state)
            self.create_plan_servic_client = self.create_client(CreatePlanSRV,"create_plan")
            self.path_sub = self.create_subscription(Path,"Path",self.get_path)
            while not self.create_plan_servic_client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info("waiting for create plan service ....")

            create_plan_requst = CreatePlanSRV.Request()
            create_plan_requst.x = msg.x_pose
            create_plan_requst.y = msg.y_pose

            self.create_plan_servic_client.call_async(create_plan_requst)\
            .add_done_callback(self.create_plan_response)

    
    def create_plan_response(self,future):
        response = future.result()
        try:
            if response.achevied:
                self.get_logger().info("plan is created successfully")
                self.state.data = "navigate state"
                self.state_pub.publish(self.state)
            else:
                self.get_logger().info("can't create plan")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")





def main(argv=None):
    rclpy.init()
    node = BehaviourNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()