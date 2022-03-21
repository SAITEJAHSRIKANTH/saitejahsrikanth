import rospy
import random
from cr_week8_test.msg import *

def interaction_generator():
	objectinteractpub = rospy.Publisher('object_info', object_info, queue_size=10)
	humaninteractpub = rospy.Publisher('human_info', human_info, queue_size=10)
	rospy.init_node('interaction_generator', anonymous=True)
	objectinteract = object_info()
	humaninteract = human_info()
	objectinteract.id = 1 # id for each interaction
	rate = rospy.Rate(0.1) 	# To generate data of object + human interaction every 10 seconds
	while not rospy.is_shutdown():
		objectinteract.object_size = random.randint(1, 2) #random object size (1=small, 2=big)
		humaninteract.id = objectinteract.id
		humaninteract.human_expression = random.randint(1, 3) #random human expression (1=happy, 2=sad, 3=neutral)
		humaninteract.human_action = random.randint(1, 3) #random human action (1=look at the robot, 2=look at the toy, 3=lookaway)

		objectinteractpub.publish(objectinteract)
		humaninteractpub.publish(humaninteract)
		
		rate.sleep()
		
		objectinteract.id += 1

if __name__ == '__main__':
	try:
		interaction_generator()
	except rospy.ROSInterruptException:
		pass
