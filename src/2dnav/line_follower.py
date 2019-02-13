#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy, math, timeit
from sensor_msgs.msg import Image, CameraInfo, LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Int32
import timeit
class Follower:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    #cv2.namedWindow("window", 1)
    self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
    self.image_sub = rospy.Subscriber('/cv_camera/image_raw', 
                                      Image, self.image_callback)
    self.cmd_vel_pub = rospy.Publisher('RosAria/cmd_vel',
                                      Twist, queue_size=1)
    self.debug = rospy.Publisher('/debug', String, queue_size=1)
    self.twist = Twist()
    self.canMove = timeit.default_timer() - 2
    self.video = cv2.VideoWriter('/home/rhys/outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
    self.video2 = cv2.VideoWriter('/home/rhys/outpy2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
    self.current = rospy.Publisher('/node', String, queue_size=1)
    self.currentlyRotating = False
    self.stopRoating_sub = rospy.Subscriber('/centeringID', Int32, self.rotate_callback)
    self.startRotating = rospy.Subscriber('/start_follow', String, self.start_callback)
    self.obstacle_count = 0
    self.l = [0] * 5


  def rotate_callback(self, ID):
	self.currentlyRotating = True

  def image_callback(self, msg):
    self.debug.publish("hello")
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    self.video2.write(image)
    
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

    

    M = cv2.moments(mask)
    #cv2.imwrite("/home/rhys/mask" + str(timeit.default_timer()) + ".png", mask)

    if M['m00'] > 0:
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])
      cv2.circle(res, (cx, cy), 20, (0,0,255), -1)
      # BEGIN CONTROL
      err = cx - w/2
      self.twist.linear.x = 0.15
      self.twist.angular.z = -float(err) / 100
      self.debug.publish(str(timeit.default_timer() - self.canMove))
     
      if timeit.default_timer() - self.canMove > 2 and not self.currentlyRotating:
        self.current.publish('trying to follow line')
      	self.cmd_vel_pub.publish(self.twist)
	
      # END CONTROL
   
    

    self.video.write(res)


  def saveVideo(self):
	self.video.release()
	self.video2.release()


  def scan_callback(self, scan):
	current = 0
	current_angle = scan.angle_min
	for i in scan.ranges:
		y = abs(math.cos(current_angle) * i)
		x = abs(math.sin(current_angle) * i)
		if x < 0.5 and y < 2:
			
			if current < 10:
				current += 1 
	#self.current.publish(str(current))
	self.l.pop(0)
	self.l.append(current)
	if sum(self.l) > 40:
		self.canMove = timeit.default_timer()

		self.current.publish('MOVE OUT OF THE WAY ')
	
			
		current_angle += scan.angle_increment
  def start_callback(self, data):
	self.currentlyRotating = False
	

def saveVideo():
	follower.saveVideo()
	

rospy.init_node('follower')
follower = Follower()
rospy.on_shutdown(saveVideo)

rospy.spin()
# END ALL
