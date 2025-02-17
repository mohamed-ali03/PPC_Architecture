#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from rclpy.action import ActionServer
from nav2_msgs.action import FollowPath

class NavigateStateNode(Node):
    def __init__(self):
        super().__init__("Navigate_State_Node")
        self.state_sub= ActionServer(
            self,
            FollowPath,
            "navigate",
            execute_callback=self.navigate)

    def navigate(self,goal_handle):
        self.get_logger().info('Executing goal...')
        
        # Simulate navigation (replace with actual logic)
        feedback_msg = FollowPath.Feedback()
        result_msg = FollowPath.Result()

        # Publish feedback (optional)
        for i in range(10):
            feedback_msg.current_pose = ...  # Set feedback data
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {feedback_msg}')
            rclpy.spin_once(self, timeout_sec=0.1)

        # Mark goal as succeeded
        goal_handle.succeed()
        result_msg.success = True
        return result_msg
        


def main(argv=None):
    rclpy.init()
    node = NavigateStateNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()