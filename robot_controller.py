import rospy
from cr_week8_test.msg import *
from cr_week8_test.srv import *
from bayesian.bbn import *

def performperception(data):
	robotexpressionpub = rospy.Publisher('robot_info', robot_info, queue_size=10)
	compute = rospy.ServiceProxy('predict_robot_expression', predict_robot_expression)
	
	robotexpression = robot_info()
	re = compute(data)
	robotexpression.id = data.id
	robotexpression.p_happy = re.p_happy
	robotexpression.p_sad = re.p_sad
	robotexpression.p_neutral = re.p_neutral

	robotexpressionpub.publish(robotexpression)
	

def robot_controller():	
	rospy.init_node('robot_controller', anonymous=True)
	rospy.wait_for_service('predict_robot_expression')
	
	rospy.Subscriber('perceived_info', perceived_info, performperception)
	
	rospy.spin()

if __name__ == '__main__':
	try:
		robot_controller()
	except rospy.ROSInterruptException:
		pass
