import unittest
import math
from spline import *
class splineTest (unittest.TestCase):
	def setUp (self):
		self.x = [0.0, 0.3, 0.5, 0.8, 1, 1.4, 1.8]
		self.y = [0.0, 0.299401, 0.4923442, 0.7228442, 0.7798934, 0.6385505, 0.4452612]
		self.spline = spline (self.x, self.y)
	
	def testCoefficients (self):
		realcoeff = [ 0, -0.08877863, -0.55472687, -2.019378, -3.56363967, -1.9027291, 0]		#  Правильные значения
		for i in range (7):
			self.assert_ (math.fabs (self.spline.m[i] - realcoeff[i]) < 1e-8)

	def testValues (self):
		x = [0.2, 0.48, 1.6, 0, 0.5]
		val = [self.spline.getValue (currx) for currx in x]
		n = len (x)		
		
		#  Правильные значения
		realVal = [0.200093881251, 0.473740862529, 0.342274119669, 0.0, 0.4923442]
		for i in range (n):
			self.assert_ (math.fabs (realVal[i] - val[i]) < 1e-10)
if __name__ == '__main__':
	unittest.main()
