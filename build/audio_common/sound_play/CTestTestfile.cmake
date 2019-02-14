# CMake generated Testfile for 
# Source directory: /home/rhys/catkin_ws/src/audio_common/sound_play
# Build directory: /home/rhys/catkin_ws/build/audio_common/sound_play
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_sound_play_nosetests_scripts.test "/home/rhys/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/kinetic/share/catkin/cmake/test/run_tests.py" "/home/rhys/catkin_ws/build/test_results/sound_play/nosetests-scripts.test.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/rhys/catkin_ws/build/test_results/sound_play" "/usr/bin/nosetests-2.7 -P --process-timeout=60 --where=/home/rhys/catkin_ws/src/audio_common/sound_play/scripts/test --with-xunit --xunit-file=/home/rhys/catkin_ws/build/test_results/sound_play/nosetests-scripts.test.xml")
subdirs(test)
