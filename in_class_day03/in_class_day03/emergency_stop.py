""" This script explores publishing ROS messages in ROS using Python """
import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist, Vector3
from neato2_interfaces.msg import Bump

class EmergencyStopNode(Node):
    """This is a message publishing node, which inherits from the rclpy Node class."""
    def __init__(self):
        """Initializes the SendMessageNode. No inputs."""
        super().__init__('bumper_estop_node')
        # Create a timer that fires ten times per second
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.cmd_loop)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Bump, 'bump', self.detection_loop, 10)
        self.bumped = False

    def cmd_loop(self):
        twist_msg = Twist(linear=Vector3(x=0.1 if not self.bumped else 0.0,y=0.0,z=0.0), angular=Vector3(x=0.0,y=0.0,z=0.0))
        self.publisher.publish(twist_msg)
        
    def detection_loop(self, msg: Bump):
        self.bumped == msg.left_front or msg.right_front or msg.left_side or msg.right_side
        twist_msg = Twist(linear=Vector3(x=0.0,y=0.0,z=0.0), angular=Vector3(x=0.0,y=0.0,z=0.0))
        self.publisher.publish(twist_msg)
        

def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)      # Initialize communication with ROS
    node = EmergencyStopNode()   # Create our Node
    rclpy.spin(node)           # Run the Node until ready to shutdown
    rclpy.shutdown()           # cleanup

if __name__ == '__main__':
    main()