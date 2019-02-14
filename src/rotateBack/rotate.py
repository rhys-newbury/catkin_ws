#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy, math, timeit
from sensor_msgs.msg import Image, CameraInfo, LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Int32
import message_filters
from tf.transformations import euler_from_quaternion

class Follower:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    self.Move = False
    self.image_sub = rospy.Subscriber('/cv_camera/image_raw', 
                                      Image, self.image_callback)
    self.cmd_vel_pub = rospy.Publisher('RosAria/cmd_vel',
                                      Twist, queue_size=1)
    self.debug = rospy.Publisher('/debug', String, queue_size=1)
    self.current = rospy.Publisher('/node', String, queue_size=1)

    self.twist = Twist()

    self.return_sub = rospy.Subscriber('/return_to_position', Int32, self.find_direction)
    self.odom_sub = rospy.Subscriber('/RosAria/pose', Odometry, self.set_callback)

    self.position = None

    self.start_line = rospy.Publisher('start_follow', String, queue_size=1)
	
    
    self.direction = 0

  def find_direction(self, rotation):
	if str(rotation.data) == "0":
		self.direction = 1
	elif str(rotation.data) == "1":
		self.direction = 1
	elif str(rotation.data) == "-1":
		self.direction = -1
	self.Move = True


  def calc_callback(self, data):
	current = self.position
	if current == None:
		return
	
	orientation_q = data.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        _, _, yaw_start = euler_from_quaternion (orientation_list)

	orientation_q = current.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        _, _, yaw_final = euler_from_quaternion (orientation_list)


	#change to 0 to 2 pi
        angle_start = yaw_start + math.pi
        #change to 0 to 360
        angle_start = angle_start * 180 / math.pi

	#change to 0 to 2 pi
        angle_final = yaw_final + math.pi
        #change to 0 to 360
        angle_final = angle_final * 180 / math.pi

       
	#angular_diff = angle_start - angle_final
	#angular_diff = (angular_diff + 180) % 360 - 180
	
	#if angular_diff < 0:
	#	self.direction = -1
	#if angular_diff > 0:
	#	self.direction = 1
        #

	if ((angle_final - angle_start + 360) % 360 < 180):
		self.direction = -1
	else:
		self.direction = 1
	self.Move = True
	

  def set_callback(self, data):
	self.position = data

  def image_callback(self, msg):
    if not self.Move:
	return
    self.current.publish('i am trying to find line')

    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
   
    
    lower_red = numpy.array([ 0,  110,  110])
    upper_red = numpy.array([10, 255, 255])
    mask1 = cv2.inRange(hsv_img, lower_red, upper_red)

    lower_red1 = numpy.array([ 170,  110,  110])
    upper_red1 = numpy.array([180, 255, 255])
    mask2 = cv2.inRange(hsv_img, lower_red1, upper_red1)

    lower_blue = numpy.array([ 100,  90,  90])
    upper_blue = numpy.array([125, 255, 255])
    mask3 = cv2.inRange(hsv_img, lower_blue, upper_blue)

    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.bitwise_or(mask, mask3)

    h, w, d = image.shape
    search_top = 3*h/4
    search_bot = 3*h/4 + 20

    res = cv2.bitwise_and(image,image,mask = mask)


    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0

    num = cv2.countNonZero(mask)


    self.debug.publish(str(num))
    if num > 200:
	self.Move = False
	self.start_line.publish('start')
    else:
	speed = Twist()
	speed.angular.z = self.direction * 0.4
	self.cmd_vel_pub.publish(speed)
		
   

  
rospy.init_node('follower')
follower = Follower()
rospy.spin()
