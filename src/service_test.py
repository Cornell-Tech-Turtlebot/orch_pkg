#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from orch_pkg.srv import *

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
		
	def name(self):
		return self.switcher.get(self.state, 'Invalid State') + '_service'

	def next(self):
		# Go from dumping to patrolling
		if self.state + 1 == self.num_states:
			self.state = 1

		# Go to next state 
		else:
			self.state = (self.state + 1) % self.num_states

#num_states = 5
#def state_name(i):
#	switcher = {
#		0: exploring
#		1: patrolling
#		2: approaching
#		3: manipulating
#		4: dumping
#	}
#	return switcher.get(i, 'Invalid State')


def orchestrator():

	# Initialize finite state machine
	fsm = FiniteStateMachine()

	# Loop infinitely
	while not rospy.is_shutdown():

		# Wait until service is running
		print('waiting on %s' % fsm.name())
		rospy.wait_for_service(fsm.name())
		print('%s initiated' % fsm.name())


		# Send the service request
		try:
			tmp_service = rospy.ServiceProxy(fsm.name(), ReqRes)
			resp = tmp_service()
			print('%s responded %s' % (fsm.name(), resp.resp))
		except rospy.ServiceException as e:
			print('%s call failed: %s' % (fsm.name(), e))

		# Update state
		fsm.next()


if __name__ == '__main__':
	try:
		orchestrator()
	except rospy.ROSInterruptException:
		print('Orchestrator Failed')
