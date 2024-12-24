from sklearn.model_selection import train_test_split                            # open-source
from sklearn.preprocessing import LabelEncoder                                  # open-source
from .data_processing import load_data, preprocess_data, feature_engineering    # self custom
from .model import train_model, evaluate_model                                  # self custom
from .config import HISTORICAL_DATA_PATH                                        # self custom


def main():
    data = load_data(HISTORICAL_DATA_PATH)
    data = preprocess_data(data)
    
    label_enc = LabelEncoder()
    X, y = feature_engineering(data, label_enc)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = train_model(X_train, y_train)
    evaluate_model(clf, X_val, y_val)


if __name__ == "__main__":
    main()




