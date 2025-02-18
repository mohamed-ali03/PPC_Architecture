#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from ppc_interfaces.srv import CreatePlanSRV
from geometry_msgs.msg import Point,PoseStamped
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry


class CreatePlanNode(Node):
    def __init__(self):
        super().__init__("Create_Plan_Node")
        self.create_plan_service_server = self.create_service(CreatePlanSRV,"create_plan",self.create_plan_callback)
        self.sub_current_pose = self.create_subscription(Odometry,"/odom",self.Current_Pose,10)
        self.current_pose = Point()

    def Current_Pose(self,msg:Odometry):
        self.current_pose.x = msg.pose.pose.position.x
        self.current_pose.y = msg.pose.pose.position.y


    def create_plan_callback(self,requst,response):
        target_point = Point(x=requst.target_pose.position.x, y=requst.target_pose.position.y)
        path = Path()

        current_pose_stamped = PoseStamped()
        current_pose_stamped.pose.position = self.current_pose
        current_pose_stamped.header.stamp = self.get_clock().now().to_msg()
        current_pose_stamped.header.frame_id = "global_planner"  # Set the frame ID

        target_pose_stamped = PoseStamped()
        target_pose_stamped.pose.position = target_point
        target_pose_stamped.header.stamp = self.get_clock().now().to_msg()
        target_pose_stamped.header.frame_id = "global_planner"  # Set the frame ID

        # Append to the path
        path.poses.append(current_pose_stamped)
        path.poses.append(target_pose_stamped)

        # Set the response
        response.achevied = True
        response.path = path
        return response 



def main(argv=None):
    rclpy.init()
    node = CreatePlanNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()