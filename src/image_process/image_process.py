#!/usr/bin/env python
import rospy
#from sensor_msgs.msg import Image
import sensor_msgs
import cv2
from std_msgs.msg import String, Int32
from google.cloud import storage
from cv_bridge import CvBridge

from PIL import Image, ImageDraw
import timeit

class TakePicture():
	def __init__(self):
		self.image_sub = rospy.Subscriber('/images', String, self.image_callback)
		self.bridge = CvBridge()
		self.debug = rospy.Publisher('/debug12', String, queue_size=1)
		self.count = 0
		self.current = rospy.Publisher('/upload', String, queue_size=1)
	def image_callback(self, image):

		cv2_image = cv2.imread(str(image.data))
		first = image.data

		height, width, _ = cv2_image.shape
		photo_count = 0
		'''		
		for i in range(1,5):
			crop_img = cv2_image[i*200:height-i*200, i*300:width-i*300].copy()
			cv2.imwrite(first + "__" + str(photo_count) + ".jpg", crop_img)
			photo_count += 1

			crop_img = cv2_image[2*i*200:height, 2*i*300:width].copy()			
			cv2.imwrite(first + "__" + str(photo_count) + ".jpg", crop_img)
			photo_count += 1

			crop_img = cv2_image[0:height-2*i*200, 2*i*300:width].copy()
			cv2.imwrite(first + "__" + str(photo_count) + ".jpg", crop_img)
			photo_count += 1

			crop_img = cv2_image[0:height-2*i*200, 0:width-2*i*300].copy()
			cv2.imwrite(first + "__" + str(photo_count) + ".jpg", crop_img)
			photo_count += 1

			crop_img = cv2_image[2*i*200:height, 0:width-2*i*300].copy()
			cv2.imwrite(first + "__" + str(photo_count) + ".jpg", crop_img)			
			photo_count += 1
			
			#cv2_image = cv2.cvtColor(cv2_image,cv2.COLOR_BGR2RGB)
	 	'''	
		#self.current.publish('starting to upload')
		#storage_client = storage.Client()

		#bucket = storage_client.get_bucket('monash-robot-photos')
    		#blob = bucket.blob(first.split("/")[-1])
		#converted = cv2.imencode('.jpg', cv2_image)[1].tostring()
		#blob.upload_from_string(converted)
		#self.current.publish('uploaded!!')
		




rospy.init_node('take_pic')
follower = TakePicture()

rospy.spin()
