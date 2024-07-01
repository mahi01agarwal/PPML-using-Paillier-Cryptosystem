import unittest
import json
import os
import sys

sys.path.append('..')

from CustomerEncrypts import storeKeys, getKeys, serializeData, preprocessData

class TestCustomerEncrypts(unittest.TestCase):
    def test_storeKeys(self):
        storeKeys()
        self.assertTrue(os.path.exists('PaillierKeys/custkeys.json'))
    
    def test_getKeys(self):
        storeKeys()
        pub_key, priv_key = getKeys()
        self.assertIsNotNone(pub_key)
        self.assertIsNotNone(priv_key)
    
    def test_serializeData(self):
        pub_key, priv_key = getKeys()
        data = [1, 2, 3]
        serialized_data = serializeData(pub_key, data)
        self.assertIsInstance(serialized_data, str)
    

if __name__ == '__main__':
    unittest.main()
