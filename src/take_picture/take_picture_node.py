#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
#from darknet_ros_msgs.msg import *
import timeit
from nav_msgs.msg import Odometry
import roslib; roslib.load_manifest('sound_play')
from sound_play.libsoundplay import SoundClient
import io
#from take_picture.msg import photo
import os
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np
import cv2
import math
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import rospy
import time
import gphoto2 as gp
import subprocess, signal
from google.cloud import storage


class TakePicture():
	def __init__(self):
		self.take_pic = False
		self.vel = rospy.Publisher('RosAria/cmd_vel', Twist, queue_size=1)
		self.current = rospy.Publisher('/node', String, queue_size=1)
		self.return_pub = rospy.Publisher('/return_to_position', Int32, queue_size=1)
		self.image_pub = rospy.Publisher('/images', String, queue_size=100)
		self.copy = rospy.Publisher('/copy', String, queue_size=20)
		self.nn_sub = None
		self.direction = None
		self.num_pics = -1
		self.factor = None
		self.count = []
		self.bridge = CvBridge()
		#self.id_sub = rospy.Subscriber("/take_pic", Odometry, self.id_callback)
    		self.last_rotated = rospy.Subscriber("/rotation", Int32, self.rotation_callback)
		self.pose_sub = rospy.Subscriber("/RosAria/pose", Odometry, self.savePose)
		self.lastDetection = None
		self.sound_client = SoundClient()
		self.imageList = []
		self.starting_pose = None
		self.starting_angle = None
		self.startRotate = True
		self.num_angles = 0
		self.first_completed = False


		p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
		out, err = p.communicate()

		for line in out.splitlines():
			if 'gphoto' in line:
				pid = int(line.split(None, 1)[0])
				os.kill(pid, signal.SIGKILL)


		self.camera, self.context = self.refresh_camera()

	def rotation_callback(self, rotation):
		self.num_pics = 0
		#sound = self.sound_client.waveSound('/home/rhys/catkin_ws/devel/audio_assets/camera.wav')
		#sound.play()

		


		if str(rotation.data) == "0":
			self.factor = 0	
		elif str(rotation.data) == "-1":
			self.factor = 1
		elif str(rotation.data) == "1":
			self.factor = -1

		self.startRotate = True
		self.current.publish("got a factor")
		#try:
		self.camera.trigger_capture(self.context)
		
		self.return_pub.publish(self.factor)	
		time.sleep(0.5)
		pics = self.list_files(self.camera)
		self.current.publish(str(pics))	
		image_list = []
		for path in pics:

			folder, name = os.path.split(path)
			dest = "/home/rhys/folder/" + name

			camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, folder, name, gp.GP_FILE_TYPE_NORMAL))
			try:
				gp.check_result(gp.gp_file_save(camera_file, dest))
				image_list.append(name)
				self.image_pub.publish(dest)
			except:
				try:
					gp.check_result(gp.gp_file_save(camera_file, dest))
					image_list.append(name)
					self.image_pub.publish(dest)
				except:
					pass
				
			
			gp.check_result(gp.gp_camera_file_delete(self.camera, folder, name))


		
			

		#storage_client = storage.Client()
		#bucket = storage_client.get_bucket('monash-robot-files')
		#blob = bucket.blob("files_" + str(timeit.default_timer()))
		#converted = str(image_list)
		#blob.upload_from_string(converted)

		gp.check_result(gp.gp_camera_exit(self.camera))
		self.camera, self.context = self.refresh_camera()
	
		self.copy.publish('done')
		
		#except Exception as e:
		#	
		#	self.current.publish(str(e))

		#	self.return_pub.publish(self.factor)
		
			
		#	time.sleep(8)

		#	self.camera, self.context = self.refresh_camera()
		#	self.copy.publish('done')

		
		

	def refresh_camera(self):
		
		context = gp.gp_context_new()
		camera = gp.check_result(gp.gp_camera_new())
		gp.check_result(gp.gp_camera_init(camera, context))

		config = camera.get_config(context)
		node = config.get_child_by_name("burstnumber")
		node.set_value(20)
		node = config.get_child_by_name("capturemode")
		node.set_value('Burst')
		node = config.get_child_by_name("capturetarget")
		node.set_value('Memory card')
		camera.set_config(config, context) 

		return camera, context

	def list_files(self, camera, path='/'):
		result = []
		# get files
		for name, value in gp.check_result(gp.gp_camera_folder_list_files(camera, path)):
			result.append(os.path.join(path, name))
		# read folders
		folders = []
		for name, value in gp.check_result(gp.gp_camera_folder_list_folders(camera, path)):
			folders.append(name)
		# recurse over subfolders
		for name in folders:
			result.extend(self.list_files(camera, os.path.join(path, name)))
    		return result

	def savePose(self, msg):
		if self.factor == None:
			return

		if not self.startRotate:
			return

		self.current.publish("receiving poses")
		orientation_q = msg.pose.pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(roll, pitch, yaw) = euler_from_quaternion (orientation_list)


		if self.starting_pose == None:
			self.starting_pose = msg
			self.starting_angle = (yaw + math.pi) * 180 / math.pi	
	
		
		#change to 0 to 2 pi
		angle = yaw + math.pi
		#change to 0 to 360
		angle = angle * 180 / math.pi

		angular_diff = 180 - abs(abs(angle - self.starting_angle) - 180); 
		self.current.publish(str(angular_diff))
		if abs(angular_diff - 55) < 5:
			self.startRotate = False
			self.starting_pose = None
			self.starting_angle = None
			self.num_pics = -1
			#sound = self.sound_client.waveSound('/home/rhys/catkin_ws/devel/audio_assets/camera.wav')
			#sound.play()
			self.current.publish('hello, i have reached position')
			
			
		else:
			speed = Twist()
			if self.factor == 0:
				speed.angular.z = (55 - angular_diff) * -0.05
			else:			
				speed.angular.z = (55 - angular_diff) * 0.05 * self.factor
			self.vel.publish(speed)

		
	def shutdown(self):
		gp.check_result(gp.gp_camera_exit(camera))
			
def shutdown():
	global follower
	follower.shutdown()

rospy.init_node('take_pic')

follower = TakePicture()
rospy.on_shutdown(shutdown)

rospy.spin()
