import rospy
import random
from cr_week8_test.msg import *

class Percept:
	def __init__(self):
		self.id = 0
		self.object_size = 0
		self.human_action = 0
		self.human_expression = 0

	def object_info(self, data):
		self.id = data.id
		self.object_size = data.object_size

	def human_info(self, data):
		self.human_action = data.human_action
		self.human_expression = data.human_expression

		self.robotperception()

	def robotperception(self):
		perception = random.randint(1, 8)
		rppub = rospy.Publisher('perceived_info', perceived_info, queue_size=10)
		
		if perception == 1:
			self.object_size = 0
		if perception == 2:
			self.human_action = 0
		if perception == 3:
			self.human_expression = 0
		if perception == 4:
			self.object_size = 0
			self.human_action = 0
		if perception == 5:
			self.object_size = 0
			self.human_expression = 0
		if perception == 6:
			self.human_action = 0
			self.human_expression = 0
		if perception == 7:
			self.object_size = 0
			self.human_action = 0
			self.human_expression = 0
		if perception == 8:
			None
		
		#print(perception)
		rppub.publish(self.id, self.object_size, self.human_action, self.human_expression)

def perception_filter():	
	rospy.init_node('perception_filter', anonymous=True)
	
	obj = Percept()
	rospy.Subscriber('object_info', object_info, obj.object_info)
	rospy.Subscriber('human_info', human_info, obj.human_info)
	
	rospy.spin()

if __name__ == '__main__':
	try:
		perception_filter()
	except rospy.ROSInterruptException:
		pass
