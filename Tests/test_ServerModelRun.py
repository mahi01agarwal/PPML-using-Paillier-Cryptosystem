import unittest
import json
import sys
import numpy as np
sys.path.append('..')
from ServerModelRun import getData, getCoef, get_Intercept, get_encryted_intercept, computeData

class TestServerModelRun(unittest.TestCase):
    def test_getData(self):
        data = getData()
        self.assertIsInstance(data, dict)
    
    def test_getCoef(self):
        coef = getCoef()
        self.assertIsInstance(coef, np.ndarray)
    
    def test_get_Intercept(self):
        intercept = get_Intercept()
        self.assertIsInstance(intercept, float)
    
    def test_get_encryted_intercept(self):
        encrypted_intercept = get_encryted_intercept()
        self.assertIsNotNone(encrypted_intercept)
    
    def test_computeData(self):
        results, pubkey = computeData()
        self.assertIsNotNone(results)
        self.assertIsNotNone(pubkey)

if __name__ == '__main__':
    unittest.main()
