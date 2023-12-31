import sys
import unittest

sys.path.append('../sorting/')

from sorting.sorts import *

class Test(unittest.TestCase):
    def init():
        unittest.main()

    def setUp(self):
        self.array=['2', '42', '57', '29', '95', '57', '4', '77', '99', '25', '73', '5', '41', '73', '99', '82', '36', '88', '42', '34', '8', '5', '83', '51', '78', '31', '11', '85', '18', '50', '7', '27', '37', '45', '99', '56', '21', '67', '2', '32', '16', '56', '53', '67', '97', '68', '55', '58', '14', '60', '37', '58', '22', '22', '56', '45', '36', '6', '92', '71', '43', '69', '18', '26', '62', '57', '12', '69', '1', '1', '49', '61', '96', '59', '78', '22', '80', '96', '82', '43', '8', '63', '93', '19', '4', '69', '83', '13', '5', '25', '98', '55', '73', '97', '16', '97', '35', '85', '40', '53']
        self.sorted_array=['1', '1', '2', '2', '4', '4', '5', '5', '5', '6', '7', '8', '8', '11', '12', '13', '14', '16', '16', '18', '18', '19', '21', '22', '22', '22', '25', '25', '26', '27', '29', '31', '32', '34', '35', '36', '36', '37', '37', '40', '41', '42', '42', '43', '43', '45', '45', '49', '50', '51', '53', '53', '55', '55', '56', '56', '56', '57', '57', '57', '58', '58', '59', '60', '61', '62', '63', '67', '67', '68', '69', '69', '69', '71', '73', '73', '73', '77', '78', '78', '80', '82', '82', '83', '83', '85', '85', '88', '92', '93', '95', '96', '96', '97', '97', '97', '98', '99', '99', '99']
        pass

    def tearDown(self):
        pass

    def test_BubleSort(self):        
        self.assertEqual(BubleSort(self.array),self.sorted_array)

    def test_ShakerSort(self):
        self.assertEqual(ShakerSort(self.array),self.sorted_array)

    def test_InsertionSort(self):
        self.assertEqual(InsertionSort(self.array),self.sorted_array)

    def test_QuickSort(self):
        self.assertEqual(QuickSort(self.array),self.sorted_array)