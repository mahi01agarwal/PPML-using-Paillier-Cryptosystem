import unittest
import json
import sys
sys.path.append('..')
from CustomerDecrypts import getKeys, loadAnswer, decryptAnswer

class TestCustomerDecrypts(unittest.TestCase):
    def test_getKeys(self):
        pub_key, priv_key = getKeys()
        self.assertIsNotNone(pub_key)
        self.assertIsNotNone(priv_key)
    
    def test_loadAnswer(self):
        answer_data = loadAnswer()
        self.assertIsInstance(answer_data, dict)
    
    def test_decryptAnswer(self):
        pub_key, priv_key = getKeys()
        answer_data = loadAnswer()
        final_prediction = decryptAnswer(pub_key, priv_key, answer_data)
        self.assertIsNotNone(final_prediction)

if __name__ == '__main__':
    unittest.main()
