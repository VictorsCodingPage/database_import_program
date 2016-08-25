import unittest
import imp

from temp_g_switch import *

class Test_Data_Sending(unittest.TestCase):
    def test_gender_switch_func_1(self):
        expected = (26, False)
        actual = switch_gender(26, "Man")
        self.assertEqual(expected, actual)

    def test_gender_switch_func_1_5(self):
        expected = (35, True)
        actual = switch_gender(39, "Man")
        self.assertEqual(expected, actual)

    def test_gender_switch_func_2(self):
        expected = (31, True)
        actual = switch_gender(15, "Man")
        self.assertEqual(expected, actual)

    def test_gender_switch_func_3(self):
        expected = (15, False)
        actual = switch_gender(15, "Women")
        self.assertEqual(expected, actual)

    def test_gender_switch_func_3_5(self):
        expected = (39, False)
        actual = switch_gender(39, "Women")
        self.assertEqual(expected, actual)

    def test_gender_switch_func_4(self):
        expected = (15, True)
        actual = switch_gender(31, "Women")
        self.assertEqual(expected, actual)
