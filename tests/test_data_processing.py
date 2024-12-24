# This file contains unit tests for the data processing module.
import unittest
import pandas as pd
from src.data_processing import preprocess_data, feature_engineering
from sklearn.preprocessing import LabelEncoder


class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'ClientID': [1, 1, 2, 2],
            'LedgerBal': [100, -50, 200, -150],
            'exclusion_status': ['yes', 'yes', 'no', 'no']
        })


    def test_preprocess_data(self):
        processed_data = preprocess_data(self.data)
        self.assertIn('total_positive_bal', processed_data.columns)
        self.assertIn('total_negative_bal', processed_data.columns)
        self.assertIn('conversion_flag', processed_data.columns)


    def test_feature_engineering(self):
        processed_data = preprocess_data(self.data)
        label_enc = LabelEncoder()
        X, y = feature_engineering(processed_data, label_enc)
        self.assertEqual(X.shape[1], 3)
        self.assertEqual(len(y), len(processed_data))


if __name__ == '__main__':
    unittest.main()




