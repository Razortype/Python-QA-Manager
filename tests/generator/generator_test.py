import unittest
import sys, os
from random import randint

from pathlib import Path
sys.path.insert(1, str(Path(os.getcwd()).parent.parent.absolute())+"/QAManager/generator/")
from generator import RandomGenerator as RG

# Random Number Tests
class TestGenerateNumber(unittest.TestCase):

    def test_wrong_decleration(self):
        """
        Initially expected condition tests
        """
        self.assertEqual(RG.number(), -999, "Indicator should be diclared")
        self.assertEqual(RG.number(inval=True,dig=True), -999, "Indivator should be declared")
        self.assertEqual(RG.number(s=5,e=1,inval=True), -999, "Start interval could not be bigger end interval")
        self.assertEqual(RG.number(length=0,dig=True), -999, "Lenght of number could not be 0")
        self.assertEqual(RG.number(length=-5,dig=True), -999, "Lenght of number could not be less than 0")

    def test_inval_number(self):
        """
        Checks if number in right interval (1000)
        """
        for _ in range(1000):
            self.assertIn(RG.number(s=5,e=10,inval=True), range(5,11), f"Number digit count must be same")
        
    def test_digit_number(self):
        """
        Checks if right digit of number occured (1000)
        """
        for _ in range(1000):
            rand_number = randint(1,1000)
            self.assertEqual(len(str(RG.number(length=rand_number,dig=True))), rand_number, f"Number digit count should be {rand_number}")

# Random String Tests
class TestGenerateString(unittest.TestCase):

    def test_wrong_decleration(self):
        """
        Initially expected condition tests
        """
        self.assertEqual(RG.string(s=5,e=1,random=True), "None", "Start interval could not be bigger end interval")
        self.assertEqual(RG.string(length=0), "None", "Lenght of string could not be 0")
        self.assertEqual(RG.string(length=-5), "None", "Lenght of string could not be less than 0")
        self.assertEqual(RG.string(s=5,e=261,random=True), "None", "Letter amount could not be bigger than 255")
        self.assertEqual(RG.string(length=256), "None", "Letter amount could not be bigger than 255")

    def test_inval_string(self):
        """
        Checks if length of string related with intervals
        """
        for _ in range(1000):
            rand_string = RG.string(s=3,e=25,random=True)
            self.assertIn(len(rand_string), range(3,26), "Length of string should be declared with interval")

    def test_length_string(self):
        """
        Checks if expected length equalt to output strign length
        """
        for length in range(1,255):
            rand_string = RG.string(length=length)
            self.assertEqual(len(rand_string), length, "Declared length should equal to string length")

# Random Boolean Tests
class TestGenerateBoolean(unittest.TestCase):

    def test_bool_case(self):
        """
        Checks if value is one of True or False value (1000)
        """
        for _ in range(1000):
            self.assertIn(RG.boolean(),[True, False],"Boolean should be equal to True or False value")

    def test_number_case(self):
        """
        Checks if value is one of 1 or 0 value (1000)
        """
        for _ in range(1000):
            rand_value = RG.boolean(number=True)
            self.assertIn(rand_value,[0,1],"Boolean should be equal to 1 or 0 value")

# Random Double Test
class TestGenerateDouble(unittest.TestCase):

    def test_wrong_decleration(self):
        self.assertEqual(RG.double(rnd=-5), -999.0, "Round value could not be less than 0")

    def test_double_case(self):
        for _ in range(1000):
            pass
        
    def test_round_case(self):
        for _ in range(1000):
            pass

if __name__ == '__main__':
    unittest.main()