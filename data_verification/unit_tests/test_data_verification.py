import unittest
import imp

data_verification = imp.load_source('data_verification', '../product_filter.py')
data_reading = imp.load_source('data_reading', '../../data_reading/scan_file_to_dict.py')

class Test_Data_Verification_Functions(unittest.TestCase):
    def setUp(self):
        self.dict_one = data_reading.scan_file_to_dict("../../CJ_Categories.csv", 3, 2, "\t")

    def test_product_filter(self):
        expected = "Accessories"
        actual_value = data_verification.product_filter("Bandanas", self.dict_one)

if __name__ == '__main__':
    unittest.main()