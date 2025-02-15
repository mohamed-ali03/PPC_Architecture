#!/usr/bin/env python

import rclpy 
from rclpy.node import Node
from rclpy.action import ActionServer
from nav2_msgs.action import FollowPath

class NavigateStateNode(Node):
    def __init__(self):
        super().__init__("Navigate_State_Node")
        self.state_sub= ActionServer(self,FollowPath,"navigate",execute_callback=self.navigate)

    async def navigate(self,target):
        feedback_msg = FollowPath.Feedback()
        result_msg = FollowPath.Result()

        path = target.Goal.path


        for i in range (1,10) :
            target.publish_feedback(i)
            await rclpy.spin_once(self, timeout_sec=0.1)


        target.succeed()
        return result_msg
        


def main(argv=None):
    rclpy.init()
    node = NavigateStateNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()