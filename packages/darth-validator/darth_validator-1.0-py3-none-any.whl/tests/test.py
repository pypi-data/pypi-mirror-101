import unittest
from validator import validator
import pandas as pd

class ValidatorTest(unittest.TestCase):
    df1 = validator.df_parser('validator/example1.xlsx')
    df2 = validator.df_parser('validator/example2.xlsx')
    
    def test_df_parser(self):
        self.assertEquals(type(ValidatorTest.df1), tuple)
        self.assertEquals(type(ValidatorTest.df1[0]), pd.DataFrame)
        self.assertEquals(type(ValidatorTest.df1[1]), str)
        self.assertEquals(ValidatorTest.df1[1], 'validator/example1')

    def test_data_lst(self):
        self.assertEquals(type(validator.data_lst(ValidatorTest.df1[0])), dict)
        self.assertEquals(len(ValidatorTest.df1[0].keys()), 5)
    
    def test_val_list_count(self):
        lst1 = validator.data_lst(ValidatorTest.df1[0])
        lst2 = validator.data_lst(ValidatorTest.df2[0])
        mlst1, ulst1, mcount1, ucount1 = validator.val_list_count(lst1, lst2)
        self.assertEquals(type(mcount1), int)
        self.assertEquals(type(ucount1), int)
        self.assertEquals(mcount1, 999)
        self.assertEquals(ucount1, 1)
        self.assertEquals(type(mlst1), list)
        self.assertEquals(type(ulst1), list)
        self.assertEquals(len(mlst1), 999)
        self.assertEquals(len(ulst1), 1)
        self.assertEquals(type(validator.val_list_count(lst1, lst2)), tuple)

if __name__ == '__main__':
    unittest.main()