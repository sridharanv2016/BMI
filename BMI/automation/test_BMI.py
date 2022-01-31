import unittest
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(1,BASE_DIR + '/code')
import BMI
from pathlib import Path
import pandas as pd


class TestBMI(unittest.TestCase):
    filename = Path(BASE_DIR + '/data/data.json')
    lookupfilename = Path(BASE_DIR + '/data/lookup.json')

    def test_fileexists(self):
        result = BMI.file_name_exists()
        self.assertEqual(result,1)

    def test_get_body_mass_index(self):
        df = pd.DataFrame({
            'WeightKg': [80],
            'HeightCm':  [140],
        })
        result = df.apply(BMI.get_body_mass_index, axis=1)
        self.assertTrue(result[0] > 0)

    def test_read_json_into_df(self):
        result = BMI.read_json_into_df()
        print(result)
        self.assertTrue('ERROR' not in result)

if  __name__ == '__main__':
    unittest.main()
