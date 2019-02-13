#!/usr/bin/env python

import roslib; roslib.load_manifest('sound_play')
import rospy
from sound_play.libsoundplay import SoundClient

rospy.init_node('play_sound_file')
#Create a sound client instance
sound_client = SoundClient()
#wait for sound_play node to connect to publishers (otherwise it will miss first published msg)
rospy.sleep(2)

#Method 2: Create Sound instance for file, play with '.play()' method
sound = sound_client.waveSound('/home/rhys/catkin_ws/devel/audio_assets/camera.wav')
sound.play()
