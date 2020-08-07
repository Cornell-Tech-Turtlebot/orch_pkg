#!/usr/bin/env python

import rospy
import roslaunch
from std_msgs.msg import String 

# Define globals
workspace_path = '/home/zacharygittelman/work_all' # TODO: use catkin_workspace or current workspace, maybe a parameter
EXPLORING_COMPLETED = False
TRASHCAN_DETECTED = False


def exploring_callback(data):
	print('CALLBACK-----------------------------------------')
	if data.data == 'completed':
		print('COMPLETED-----------------------------------------')
		global EXPLORING_COMPLETED
		EXPLORING_COMPLETED = True

def trashcan_callback(data):
	if data.data == 1: # TODO: potentially change 1 to True
		global TRASHCAN_DETECTED
		TRASHCAN_DETECTED = True


class FiniteStateMachine:

	def __init__(self):
		self.state = 0
		self.num_states = 6
		self.switcher = {
			0: 'exploring',
			1: 'patrolling',
			2: 'approach_trash',
			3: 'pickup_trash',
			4: 'approach_trashcan',
      			5: 'dumping_trash'
		}
		
	def get_state(self):
		s = self.switcher.get(self.state, 'Invalid State')
		return String(s)

	def next(self):

		# Explore only once, then go to patrolling
		if self.state == 0:
			
			print('STATE0 ------------------------------------------------')

			# Move to Patrolling 
			if EXPLORING_COMPLETED:

			        print('DONE EXPLORING--------- ------------------------------------------------')

				# Launch navigation
				path = workspace_path + '/src/turtlebot3_navigation/launch/turtlebot3_navigation_orch.launch'
				uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
				roslaunch.configure_logging(uuid)
				launch = roslaunch.parent.ROSLaunchParent(uuid, [path]) 
				launch.start()
				rospy.loginfo('navigation launched')

				# Run patrol file
				package = 'patrol'
				executable = 'random_nav_orch.py'
				node = roslaunch.core.Node(package, executable)
				launch = roslaunch.scriptapi.ROSLaunch()
				launch.start()
				process = launch.launch(node)
				# TODO: process.stop()???

				# Increment state
				self.state += 1

		# Patrolling
		elif self.state == 1:

			# THIS IS ALL DONE IN orch LAUNCH FILE	
			# Launch apriltag
			# roslaunch apriltag_ros continuous_detection.launch
			# Run trashcan tracking
			# rosrun object_tracking detect_trashcan.py
			# rosrun object_tracking find_trashcan.py

			# Start looking for water bottle
			if TRASHCAN_DETECTED:	
				pass			

				# TODO: run find_trash.py
				# TODO: add qrcode to turtlebot3_gazebo turtlebot3_world.launch

				# Run 2 below: look for water bottle
				# roslaunch darknet_ros darknet_ros.launch
				# rosrun object_tracking find_trash.py

			# Switch to approaching trash
			# if trashcan_detected and /trash_detected: True:
				# switch to state2=approaching_trash

		# Approach trash
		elif self.state == 2:
			pass			
			# subscribe /trash_approached: True
				# switch to state3=pickup_trash

		# Pickup trash
		elif self.state == 3:
			pass			
			# subscribe /trash_picked_up: True 
				# switch to state4=approaching_trashcan

		# Approaching trashcan
		elif self.state == 4:
			pass			
			# subscribe /trashcan_approached: True
				# switch to state5=dumping_trash

		# Dumping trash
		else:
			pass			
			# subscribe /trash_dumped: True
				# switch to state1=patrolling	
		

		## Go to next state 
		#elif self.state + 1 < self.num_states:
		#	self.state += 1 

		## Restart the cycle excluding exploring, go from dumping to patrolling
		#else:
		#	self.state = 1



def orchestrator():

	# Initialize subscribers
	rospy.Subscriber('exploring_completed', String, exploring_callback)

	# Initialize publisher
	rospy.init_node('orch_node')
	pub = rospy.Publisher('state', String, queue_size=10)
	r = rospy.Rate(0.2) # 5hz
	

	# Initialize finite state machine
	fsm = FiniteStateMachine()

	# Loop infinitely
	while not rospy.is_shutdown():

		# Publish state
		pub.publish(fsm.get_state())

		# Update state
		fsm.next()

		# Publish at specified rate
		r.sleep()


if __name__ == '__main__':
	orchestrator()
