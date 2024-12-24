# This file contains the model training, evaluation, and prediction logic.
#from sklearn.pipeline import Pipeline
#from sklearn.compose import ColumnTransformer
#from sklearn.preprocessing import StandardScaler
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import classification_report, roc_auc_score
#import joblib
import logging
import pandas



def analysis_pack(data, ex_col):

    df= data[ex_col].agg(['mean','min','max','std','var','count','sum','quantile'])
    #print(df)
    #df.to_excel('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\tests\\precal\\analysis_result.xlsx', index=True) # if save excel sheet name will sheet1
    return df





'''
logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


def train_model(X_train, y_train):
    numeric_features = ['total_positive_bal', 'total_negative_bal']
    categorical_features = ['exclusion_status']
    
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features)
        ],
        remainder='passthrough'
    )
    
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    clf.fit(X_train, y_train)
    joblib.dump(clf, MODEL_PATH)
    logging.info(f"Model trained and saved to {MODEL_PATH}")
    return clf


def evaluate_model(clf, X_val, y_val):
    y_pred = clf.predict(X_val)
    report = classification_report(y_val, y_pred)
    roc_auc = roc_auc_score(y_val, y_pred)
    
    logging.info("Model Evaluation Report:\n" + report)
    logging.info(f"ROC AUC Score: {roc_auc:.4f}")
    
    return roc_auc


def load_model():
    try:
        clf = joblib.load(MODEL_PATH)
        logging.info(f"Model loaded from {MODEL_PATH}")
        return clf
    except Exception as e:
        logging.error(f"Error loading model from {MODEL_PATH}: {e}")
        raise


def predict_new_data(clf, new_data, label_enc):
    new_data = preprocess_data(new_data)
    new_data['exclusion_status'] = label_enc.transform(new_data['exclusion_status'])
    
    features = ['total_positive_bal', 'total_negative_bal', 'exclusion_status']
    new_day_X = new_data[features]
    
    new_data['conversion_flag'] = clf.predict(new_day_X)
    
    return new_data
'''


