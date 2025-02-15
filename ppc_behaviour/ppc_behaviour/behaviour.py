#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from ppc_interfaces.msg import MissionMSG
from std_msgs.msg import String
from ppc_interfaces.srv import CreatePlanSRV
from nav_msgs.msg import Path
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from nav2_msgs.action import FollowPath

class BehaviourNode(Node):
    def __init__(self):
        super().__init__("BehaviourNode")
        self.mission_sub = self.create_subscription(MissionMSG,"mission",self.behaviour_callback,10)
        self.state_pub = self.create_publisher(String,"state",10)
        self.state = String()
        self.state.data = "idle"
        self.state_pub.publish(self.state)

    def behaviour_callback(self,msg:MissionMSG):
        if msg.mission_name == "Stop":
            self.state.data = "idle"
            self.state_pub.publish(self.state)
        elif msg.mission_name == "GoTo":
            # create plan
            self.Cearte_plan(msg)

            

    
    def Cearte_plan(self,msg:MissionMSG):
        self.state.data = "create plan"
        self.state_pub.publish(self.state)
        self.create_plan_servic_client = self.create_client(CreatePlanSRV,"create_plan")
        while not self.create_plan_servic_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for create plan service ....")

        create_plan_requst = CreatePlanSRV.Request()
        create_plan_requst.target_pose.position.x = msg.target_pose.position.x
        create_plan_requst.target_pose.position.y = msg.target_pose.position.y

        self.create_plan_servic_client.call_async(create_plan_requst)\
        .add_done_callback(self.create_plan_response)


    
    def create_plan_response(self,future):
        response = future.result()
        try:
            if response.achevied:
                self.get_logger().info("plan is created successfully")
                self.navigate(response.path)
            else:
                self.get_logger().info("can't create plan")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")



    def navigate(self,path:Path):
        self.state.data = "navigate"
        self.state_pub.publish(self.state)
        self.navigate_action_client = ActionClient(self,FollowPath,'navigate')
        while not self.navigate_action_client.wait_for_server(1.0):
            self.get_logger().info("Waiting for navigate server available......")
        goal_msg = FollowPath().Goal()
        goal_msg.path = path 
        goal_msg.controller_id = "winner"
        self.navigate_action_client.send_goal_async(goal_msg).add_done_callback(self.navigate_goal_response)

        
    def navigate_goal_response(self,future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Navigate Goal rejected')
            return

        self.get_logger().info('Navigate Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.navigate_result_callback)
    
    def navigate_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Navigation complete!')


    def feedback_callback(self,feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(feedback)

def main(argv=None):
    rclpy.init()
    node = BehaviourNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()