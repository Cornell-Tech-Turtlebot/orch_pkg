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
		
	def get_state(self):
		s = self.switcher.get(self.state, 'Invalid State')
		return String(s)

	def next(self):
		# Explore only once
		if self.state == 0:
			# TODO: move from explore to patrol, read explore is comleted
			pass

		# Go from dumping to patrolling
		if self.state + 1 == self.num_states:
			self.state = 1

		# Go to next state 
		else:
			self.state = (self.state + 1) % self.num_states


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

		# TODO: Add logic to update state properly
		# Update state
		fsm.next()

		# Publish at specified rate
		r.sleep()


if __name__ == '__main__':
	orchestrator()
