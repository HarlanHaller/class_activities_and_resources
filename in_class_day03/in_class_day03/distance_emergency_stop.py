""" This script explores publishing ROS messages in ROS using Python """
import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

class ProximityStopNode(Node):
    """This is a message publishing node, which inherits from the rclpy Node class."""
    def __init__(self):
        """Initializes the SendMessageNode. No inputs."""
        super().__init__('proximity_estop_node')
        # Create a timer that fires ten times per second
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.cmd_loop)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(LaserScan, 'scan', self.detection_loop, 10)
        self.too_close = False
        self.stopping_distance = 0.15
        self.sensor_to_front = 0.25

    def cmd_loop(self):
        twist_msg = Twist(linear=Vector3(x=0.1 if not self.too_close else 0.0,y=0.0,z=0.0), angular=Vector3(x=0.0,y=0.0,z=0.0))
        self.publisher.publish(twist_msg)
        
    def detection_loop(self, msg: LaserScan):
        range_array = np.array(msg.ranges)
        problem_array = np.logical_and((range_array > self.sensor_to_front),  (range_array < self.sensor_to_front + self.stopping_distance))
        self.too_close = np.any(problem_array[0:45]) or np.any(problem_array[315:360])

        

def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)      # Initialize communication with ROS
    node = ProximityStopNode()   # Create our Node
    rclpy.spin(node)           # Run the Node until ready to shutdown
    rclpy.shutdown()           # cleanup

if __name__ == '__main__':
    main()