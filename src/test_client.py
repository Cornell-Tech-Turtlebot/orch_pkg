#!/usr/bin/python

import rospy
from std_msgs.msg import String
from rospy_tutorials.srv import *

def status_out():
	rospy.init_node('orch', anonymous=True)
	pub = rospy.Publisher('status_out', String, queue_size=10)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		msg_out = "hello world %s" % rospy.get_time()
		rospy.loginfo(msg_out)
		pub.publish(msg_out)
		rate.sleep()

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def status_in():
	rospy.init_node('orch', anonymous=True)
	rospy.Subscriber('status_in', String, callback)
	rospy.spin()


"""
EVERYTING ABOVE WAS FOR TESTING
"""

def orchestrator():
	print('waiting on service')
	rospy.wait_for_service('add_two_ints')
	print('service initiated')
	try:
		add_two_ints = rospy.Service('add_two_ints', AddTwoInts)
		resp1 = add_two_ints(5, 10)
		print('answer = ' + resp1.sum)
	except rospy.ServiceException as e:
		print('Service call failed: %s' % e)


if __name__ == '__main__':
	try:
		#status_out()
		#status_in()
		print('run that shit')
		orchestrator()
	except rospy.ROSInterruptException:
		print('fuck')
		pass
