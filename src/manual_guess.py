from utils import Common_Utils                                                      # same folder no need "." before utils
#from data_processing import load_bal_data, preprocess_bal_data, preprocess_cancelccy#, feature_engineering    # self custom # from folder.module import class/def/var. 
import data_processing as dp
#from .model import train_model, evaluate_model                                     # self custom 
import config                                # self custom
import model



def main():

    dd, session = Common_Utils.select_date_and_session() # class.def
    path = config.BAL_PATH(dd,session)
    rate = config.latest_rate(dd)
    df = dp.load_bal_data(path)
    # for Review: add df = df - real transaction list here
    df = dp.preprocess_bal_data(df) # doing it duty up to here
    
    ##### new raw start here #####
    df = dp.preprocess_cancelccy(df) # ok now, by change df's ClientID from obj into int for matching cancelccy_list
    df = dp.preprocess_pivot(df)
    df, created_col = dp.shortage_exchange(df,rate)
    Common_Utils.export_result(config.pivot_result_path,df) 
    #Common_Utils.export_result(config.pivot_to_share,df)
    df_analysis = model.analysis_pack(df, created_col)
    Common_Utils.export_result(config.analysis_result_path,df_analysis)
    #Common_Utils.export_result(config.analysis_to_share,df_analysis)


    
    #df.to_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\tests\\precal\\pivot_'+ dd +'_.csv', encoding='utf-8', index=False)
    
    
    '''
    label_enc = LabelEncoder()
    X, y = feature_engineering(data, label_enc)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = train_model(X_train, y_train)
    evaluate_model(clf, X_val, y_val)
    '''


if __name__ == "__main__":
    main()




