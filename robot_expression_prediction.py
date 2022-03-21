import rospy
import random
from cr_week8_test.msg import *
from cr_week8_test.srv import *
from bayesian.bbn import *
from bayesian.utils import make_key
from bayesian.exceptions import *

def f_O(O): # robot can perceive the size of the object (1=small 2=big)
	return 1.0/2.0

def f_HE(HE): # robot can percieve human facial expression (1=happy 2=sad 3=neutral)
	return 1.0/3.0

def f_HA(HA): # robot can percieve human head and eye movements (1=looking at the robot 2=looking at the colored toy 3=looking away) 
	return 1.0/3.0
    
def f_RE(O, HA, HE, RE): # robot face can express 3 possible emotions (1=happy 2=sad 3=neutral)
	if RE == '1':
		if HE == '1' and HA == '1':
			if O == '1':
				return 0.8
			elif O == '2':
				return 1
		if HE == '1' and HA == '2':
			if O == '1':
				return 0.8
			elif O == '2':
				return 1
		if HE == '1' and HA == '3':
			if O == '1':
				return 0.6
			elif O == '2':
				return 0.8
		
		if HE == '2' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0
		if HE == '2' and HA == '2':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.1
		if HE == '2' and HA == '3':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.2

		if HE == '3' and HA == '1':
			if O == '1':
				return 0.7
			elif O == '2':
				return 0.8
		if HE == '3' and HA == '2':
			if O == '1':
				return 0.8
			elif O == '2':
				return 0.9
		if HE == '3' and HA == '3':
			if O == '1':
				return 0.6
			elif O == '2':
				return 0.7
	
	if RE == '2':
		if HE == '1' and HA == '1':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '2':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.2
		
		if HE == '2' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '2' and HA == '2':
			if O == '1':
				return 0.1
			elif O == '2':
				return 0.1
		if HE == '2' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.2

		if HE == '3' and HA == '1':
			if O == '1':
				return 0.3
			elif O == '2':
				return 0.2
		if HE == '3' and HA == '2':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.1
		if HE == '3' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.2
	if RE == '3':
		if HE == '1' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '2':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.0
		
		if HE == '2' and HA == '1':
			if O == '1':
				return 1.0
			elif O == '2':
				return 1.0
		if HE == '2' and HA == '2':
			if O == '1':
				return 0.9
			elif O == '2':
				return 0.8
		if HE == '2' and HA == '3':
			if O == '1':
				return 0.8
			elif O == '2':
				return 0.6

		if HE == '3' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '3' and HA == '2':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '3' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.1


def implement(data):
	p = data.info
	
	O = str(p.object_size)
	HA = str(p.human_action)
	HE = str(p.human_expression)

	robot_bbn = build_bbn(
		f_O,
		f_HA,
		f_HE,
		f_RE,
		domains=dict(
			O = ['1', '2'],		
			HA = ['1', '2', '3'],
			HE = ['1', '2', '3'],
			RE = ['1', '2', '3']))	
	
	if O =='0' and HA == '0' and HE == '0':
		robot = robot_bbn.query()
	elif O == '0' and HA == '0':
		robot = robot_bbn.query(HE=HE)
	elif O == '0' and HE == '0':
		robot = robot_bbn.query(HA=HA)
	elif HA == '0' and HE == '0':
		robot = robot_bbn.query(O=O)
	elif HE == '0':
		robot = robot_bbn.query(O=O, HA=HA)
	elif HA == '0':
		robot = robot_bbn.query(O=O, HE=HE)
	elif O == '0':
		robot = robot_bbn.query(HA=HE, HE=HE)

	perc = {n[1]:v for n,v in robot.items() if n[0]=='RE'}	
	
	return predict_robot_expressionResponse(p.id, perc['1'], perc['2'], perc['3'])


def robot_expression_prediction():	
	rospy.init_node('robot_expression_prediction', anonymous=True)
	
	s = rospy.Service('predict_robot_expression', predict_robot_expression, implement)
	
	rospy.spin()

if __name__ == '__main__':
	try:
		robot_expression_prediction()
	except rospy.ROSInterruptException:
		pass
