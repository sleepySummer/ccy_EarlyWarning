import unittest
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from src.model import train_model, evaluate_model, predict_new_data
from src.data_processing import preprocess_data, feature_engineering


class TestModel(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'ClientID': [1, 1, 2, 2],
            'LedgerBal': [100, -50, 200, -150],
            'exclusion_status': ['yes', 'yes', 'no', 'no']
        })
        self.processed_data = preprocess_data(self.data)
        self.label_enc = LabelEncoder()
        self.X, self.y = feature_engineering(self.processed_data, self.label_enc)


    def test_train_model(self):
        clf = train_model(self.X, self.y)
        self.assertIsNotNone(clf)


    def test_predict_new_data(self):
        clf = train_model(self.X, self.y)
        new_data = predict_new_data(clf, self.processed_data, self.label_enc)
        self.assertIn('conversion_flag', new_data.columns)


if __name__ == '__main__':
    unittest.main()
