# This file handles data loading, preprocessing, and feature engineering.
import pandas as pd
import logging    # pyhton build-in Lib
import config     # from folder.module import function/class/variable




logging.basicConfig(level=config.LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


def load_bal_data(file_path):
    try:
        data = pd.read_csv(file_path, skiprows=3)  # specific setting for FOCCP file # without note++ edit, the ClientID remain obj ??
        logging.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        raise

def preprocess_bal_data(data):
    
    data = data.drop(['BRANCHID','BRANCHNAME','BASECCY','SYSTEMBASECCY','INVESTORTYPEID','PRODUCTID','CDAILYOPENBAL','DUE','AVAILABLEBAL','ACCRUEDINTEREST', 'SCDAILYOPENBAL', 'SCSETTLED', 'SPEND', 'SDUE', 'SAVAILABLEBAL', 'SLEDGERBAL', 'SHOLD', 'SRESERVE', 'SACCRUEDINTEREST'], axis=1)
    data.columns = ['ClientID', 'TradingACCSEQ', 'Name', 'ae_ID', 'INVDESC', 'CCY', 'On_Hand', 'non_settle_trade', 'LedgerBal', 'Hold', 'Reserve']
    
    # include "C" a/c edit here, keep everyting obj 
    #data_mid = data.loc[(~(data['ae_ID'].isin(['DUMMY','ED02','9999RST','ED01RST']))&(data['On_Hand']<0)&~(data['ClientID'].isin(['C209868'])))] # Origin: may be solely depend on 'LedgerBal<0'
    data_mid = data.loc[(~(data['ae_ID'].isin(['DUMMY','ED02','9999RST','ED01RST']))&(data['On_Hand']<0)&~(data['ClientID'].str.contains("C")))] # filter out all "C2xxxxx" a/c

    short_list = data_mid['ClientID'].unique() # a list who involve negative On_Hand but need find back their positive other ccy
    # short_list = obj ['079185' '205928' '108186' ... '915136' '211886' '913519']
    data = data[data['ClientID'].isin(short_list)] # 3460, filter back the original data set ### still hv bug, single client ccy row give out
    
    ## take out single ID and with HKD only
    id_counts = data['ClientID'].value_counts() # Name: count, Length: 3121, dtype: int64
    single_id = id_counts[id_counts == 1].index # Index(['xxxxxx',...,'132588'],dtype='object', name='ClientID', length=2848) 
    mask = (data['ClientID'].isin(single_id))&(data['CCY']=='HKD') # who hv ONE ccy a/c and that a/c is HKD, so if client A hv HKD -$100,00 and USD $0, he still not filter out which is correct !
    data=data[~mask] # 620, ClientID object,so far so gd
    
    return data

def preprocess_cancelccy(data):

    df_filter = pd.read_csv(config.Cancel_Path) # once ".to_csv" b4, all 009234 become 9234
    short_list = df_filter['ClntCode'].unique()
    data['ClientID'] = data['ClientID'].astype(int) # data never .to_csv and read_csv back, so keep obj, need .astype(int) here
    data = data[~(data['ClientID'].isin(short_list))]

    return data

def preprocess_pivot(data):

    
    #data = data.pivot_table(index='ClientID', columns='CCY', values='On_Hand', aggfunc='sum')
    # [USD CNH HKD JPY AUD EUR GBP CHF SGD CAD NZD] try add a complete list here
    # may try below if also want keep "ae_ID" column:
    data = data.pivot_table(index=['ClientID', 'ae_ID'], columns='CCY', values='On_Hand', aggfunc='sum')#.reset_index()

    # Fill NaN values with 0 (in case a ClientID doesn't have a value for a specific currency)
    data = data.fillna(0)
    # Reindex the columns to include all possible currencies, filling missing ones with 0
    data = data.reindex(columns=config.ccy_order_list, fill_value=0) # .reindex() auto trace if original column hv, missing will added, becoz some ccy eg CHF that round no one have
    # Reset index to turn the pivot table back into a DataFrame
    data.reset_index(inplace=True)


    return data

def convert_currency(row, source_currency, target_currency, exchange_rates):

        rate = exchange_rates.get((source_currency, target_currency))
        if rate is not None and (row[target_currency] < 0) and (source_currency =="HKD" or row[source_currency] > 0): # source HKD can negative vs other source must >0
            if source_currency =="HKD":
                transaction = row[target_currency] * rate # -usd -100,000 * 7.7941
                # logic bug, cont... here
                row[source_currency+'_'+target_currency+'_debit'] = transaction
                row[source_currency+'_'+target_currency+'_credit'] = -1*row[target_currency]
                row[source_currency] = row[source_currency] + transaction
                row[target_currency] = 0
            else:
                if abs(row[target_currency] * rate) > row[source_currency]: # (+10000)usd_to_hkd(-1,000,000) : abs(-1m) * 0.128
                    transaction = row[source_currency]*1/rate

                    row[source_currency+'_'+target_currency+'_debit'] = -1*row[source_currency] 
                    row[source_currency+'_'+target_currency+'_credit'] = transaction
                    row[source_currency] = 0
                    row[target_currency] = row[target_currency] + transaction
                else: # (+100,000)usd_to_hkd(-100,000) : abs(-100k) * 0.128
                    transaction = row[target_currency] * rate # negative num in term of [source]

                    row[source_currency+'_'+target_currency+'_debit'] = transaction
                    row[source_currency+'_'+target_currency+'_credit'] = -1*row[target_currency]
                    row[source_currency] = row[source_currency] + transaction
                    row[target_currency] = 0 # this set same as =="HKD" package


            return row
        return row

def shortage_exchange(data,pass_rates):
    '''
    direction example:
    ( -   ,   +  ) = 
    exchange_rates = {
    ('HKD', 'CNY'): 1.0876,      
    ('HKD', 'USD'): 7.7941,      
    ('USD', 'HKD'): 1/7.7941,  
    # Add more pairs as needed
    }
    '''
    exchange_rates = pass_rates
    # Apply the conversion with a lambda function to pass the additional arguments
    data = data.apply(lambda row: convert_currency(row, 'HKD', 'CNY', exchange_rates), axis=1) # am # if no -CNY, no two "HKD_CNY" created
    data = data.apply(lambda row: convert_currency(row, 'HKD', 'USD', exchange_rates), axis=1) # pm1
    data = data.apply(lambda row: convert_currency(row, 'USD', 'HKD', exchange_rates), axis=1) # pm2
    data = data.apply(lambda row: convert_currency(row, 'CNY', 'HKD', exchange_rates), axis=1) # pm3 
    # pm3, other positive ccy fill into negative hkd

    
    # Step 2: Identify all the dynamically generated columns (e.g., currency conversion columns)
    dynamic_columns = [col for col in data.columns if col not in config.col_order_list]

    # Optionally, sort dynamic columns alphabetically or by any other criteria
    dynamic_columns.sort()

    # Step 3: Combine static and dynamic columns to get the final column order
    final_column_order = config.col_order_list + dynamic_columns

    # Step 4: Reorder the DataFrame columns
    data = data.reindex(columns=final_column_order,fill_value=0) # cut out column if not exist in the list

    # time-stamp column
    data['timestamp'] = pd.Timestamp("now")
    #data.reset_index(inplace=True)
    #print(dynamic_columns)
    #data.to_csv(config.pivot_result_path, encoding='utf-8', index=False) # if save csv sheet name become pivot
    return data, dynamic_columns



'''
def preprocess_data(data):
    data = data.copy()
    data.fillna(method='ffill', inplace=True)
    
    data['total_positive_bal'] = data.groupby('ClientID')['LedgerBal'].transform(lambda x: x[x > 0].sum())
    data['total_negative_bal'] = data.groupby('ClientID')['LedgerBal'].transform(lambda x: x[x < 0].sum())
    data['conversion_flag'] = ((data['total_positive_bal'] > 0) & (data['total_negative_bal'] < 0)).astype(int)
    
    return data


def feature_engineering(data, label_enc):
    data['exclusion_status'] = label_enc.fit_transform(data['exclusion_status'])
    
    features = ['total_positive_bal', 'total_negative_bal', 'exclusion_status']
    target = 'conversion_flag'
    
    X = data[features]
    y = data[target]
    
    return X, y
'''



