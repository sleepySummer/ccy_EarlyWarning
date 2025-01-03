# This file contains configuration constants.
import os
import pandas as pd
import time
import calendar
from datetime import date
import directory as dir_string


# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) # C:\Users\Ichi\Desktop\quick_py\TTL_api


def BAL_PATH(x,y):
    path = os.path.join(BASE_DIR, 'data', 'raw', 'FOCCP_'+ x +'_'+ y +'.csv') # C:\Users\Ichi\Desktop\quick_py\TTL_api\data\raw\FOCCP_historical_data.csv
    return path


source_folder =  dir_string.import_dir + "temp/"
destin_folder = dir_string.import_dir + "cleaned/"
target_file_name = 'client_bal.csv'
cleaned_file_name = "Client_balance_" +  str(date.today()).replace("-", "") +".csv"
auto_source_path = os.path.join(source_folder, target_file_name)
auto_destin_path = os.path.join(destin_folder, cleaned_file_name)

Cancel_Path = os.path.join(BASE_DIR, 'data', 'support','cancelccy_list.csv')

pivot_result_path = os.path.join(BASE_DIR, 'result', 'predictive','pivot_exchanged_.csv')
pivot_to_share = dir_string.intermediate_dir + "early_warn/temp/pivot_exchanged_.csv"

analysis_result_path = os.path.join(BASE_DIR, 'result', 'predictive','analysis_result.xlsx')
analysis_to_share = dir_string.intermediate_dir + "early_warn/temp/analysis_result.xlsx"

ccy_order_list = ['HKD','USD','CNY','EUR','GBP','AUD','NZD','CAD','CHF','SGD','JPY']

col_order_list = ['ClientID','HKD','USD','CNY','EUR','GBP','AUD','NZD','CAD','CHF','SGD','JPY']
# col_order_list = ['ClientID','ae_ID','HKD','USD','CNY','EUR','GBP','AUD','NZD','CAD','CHF','SGD','JPY']

other_ccy = ['EUR','GBP','AUD','NZD','CAD','CHF','SGD','YEN'] # for "FXDaily_Transactions_yymmdd", JPY->YEN

review_path = os.path.join(BASE_DIR, 'result', 'review','transact_.csv')


def latest_rate(folder_date):
    
    target_folder = dir_string.intermediate_dir + folder_date[:4] +"/" + calendar.month_name[int(folder_date[4:6])][:3] + " " + folder_date[:4] + "/Records/"

    latest_file = max(os.path.join(root, filename)
                    for root, _, files in os.walk(target_folder)
                    for filename in files)

    all_files = [(os.path.join(root, filename), os.stat(os.path.join(root,filename)).st_mtime)
                    for root, _, files in os.walk(target_folder)
                    for filename in files]

    

    # any file is opened, [-1] will change to that one
    latest_source = all_files[-1][0]
    # latest_source = all_files[-2][0] # can by pass if anyone opened a file in \record\ folder, maybe a try error loop to trace back the latest usable one
    

    df = pd.read_excel(latest_source, sheet_name='Client Rate')
    df = df.drop(['Cost Ask', 'Cost Bid', 'Special Bid', 'Special Ask', 'Special Bid'], axis=1)
    df.columns = ['pair', 'Bid', 'Ask']
    #df['pair'] = df['pair'].str.replace('CNH','CNY')
    df[['source_currency', 'target_currency']] = df['pair'].str.replace('CNH','CNY').str.split('/', expand=True) # replace combine with split one line
    df = df.reindex(columns=['source_currency', 'target_currency','Bid', 'Ask'])

    reverse_df = df.copy()
    reverse_df['rate'] = reverse_df['Ask']
    reverse_df[['source_currency', 'target_currency']] = reverse_df[['target_currency', 'source_currency']] # no creat two new column, just exchange position

    df['rate'] = 1/df['Bid']

    combined_df = pd.concat([df, reverse_df])
    combined_df = combined_df.drop(['Bid','Ask'],axis=1)

    # Convert the combined DataFrame to a dictionary
    exchange_rates = {(row['source_currency'], row['target_currency']): row['rate']
                    for index, row in combined_df.iterrows()}

    return exchange_rates


'''
NEW_DAY_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'FOCCP_everynewday_day.csv')

EX_OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'FOCCP_everynewday_ex.csv')
NOT_EX_OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'FOCCP_everynewday_not_ex.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
'''

# Logging
LOGGING_LEVEL = 'INFO'


