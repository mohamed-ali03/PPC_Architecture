#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from ppc_interfaces.srv import CreatePlanSRV
from geometry_msgs.msg import Point

class CreatePlanNode(Node):
    def __init__(self):
        super().__init__("CreatePlanNode")
        self.create_plan_service_server = self.create_service(CreatePlanSRV,"create_plan",self.create_plan_callback)
        

    def create_plan_callback(self,requst,response):
        point = Point(x=requst.x, y=requst.y)

        # Global planner
        response.achevied = False
        return response 



def main(argv=None):
    rclpy.init()
    node = CreatePlanNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()