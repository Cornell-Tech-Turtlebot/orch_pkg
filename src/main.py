#!/usr/bin/env python

import rospy
import roslaunch
from std_msgs.msg import String 

class FiniteStateMachine:

	def __init__(self):
		self.state = 0
		self.num_states = 5
		self.switcher = {
			0: 'exploring',
			1: 'patrolling',
			2: 'approaching',
			3: 'manipulating',
			4: 'dumping'
		}
		self.exploring_completed = False
		self.exploring_subscribed = False
		
	def get_state(self):
		s = self.switcher.get(self.state, 'Invalid State')
		return String(s)

	def mark_completed(self, data):
		print('CALLBACK-----------------------------------------')
		if data.data == 'completed':
			print('COMPLETED-----------------------------------------')
			self.exploring_completed = True

	def next(self):
		# Explore only once, then go to patrolling
		if self.state == 0:
			
			print('STATE0 ------------------------------------------------')
			# Initialize subscriber
			if self.exploring_subscribed == False:
				rospy.Subscriber('exploring_completed', String, self.mark_completed)
			        print('SUBSCRIBED--------- ------------------------------------------------')
				self.exploring_subscribed = True

			# Launch turtlebot3_navigation, as part of next state		
			if self.exploring_completed:
				# TODO: change path to catkin_ws
			        print('DONE EXPLORING--------- ------------------------------------------------')
				path = '/home/zacharygittelman/work_all/src/turtlebot3_navigation/launch/turtlebot3_navigation_orch.launch'
				uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
				roslaunch.configure_logging(uuid)
				launch = roslaunch.parent.ROSLaunchParent(uuid, [path]) 
				launch.start()
				rospy.loginfo('navigation launched')

				# Increment state
				self.state += 1

		# Go to next state 
		elif self.state + 1 < self.num_states:
			self.state += 1 

		# Restart the cycle excluding exploring, go from dumping to patrolling
		else:
			self.state = 1



def orchestrator():

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
