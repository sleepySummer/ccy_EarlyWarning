import pandas as pd

#df = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\cash&stock_FOclientcash_csv_pritsvmsfuture_formattext_edit.csv') # must del first 3line to let column name as 1st row

x = input('Date(yyyymmdd):')
y = input('night/day:')

df = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\data\\raw\\FOCCP_'+ x +'_'+ y +'.csv', skiprows=3) # must del first 3line to let column name as 1st row
#df = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\FOCCP_20240724_night.csv')

# ref:　df = pd.read_excel('Book1.xlsx',sheetname='Sheet1',header=0,converters={'names':str,'ages':str})
df_ex = pd.read_excel('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\data\\raw\\conversion_list_'+ x +'.xlsx',header=0,converters={'ClntCode':str})
#df_ex = pd.read_excel('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\conversion_list_20240724.xlsx')
 
#df.info()
#print(list(df.columns.values)) # return column name

df_1st_drop = df.drop(['BRANCHID','BRANCHNAME','BASECCY','SYSTEMBASECCY','INVESTORTYPEID','PRODUCTID','CDAILYOPENBAL','DUE','AVAILABLEBAL','ACCRUEDINTEREST', 'SCDAILYOPENBAL', 'SCSETTLED', 'SPEND', 'SDUE', 'SAVAILABLEBAL', 'SLEDGERBAL', 'SHOLD', 'SRESERVE', 'SACCRUEDINTEREST'], axis=1)
#df_1st_drop.info()

df_1st_drop.columns = ['ClientID', 'TradingACCSEQ', 'Name', 'ae_ID', 'INVDESC', 'CCY', 'On_Hand', 'non_settle_trade', 'LedgerBal', 'Hold', 'Reserve']
#df_short = df_1st_drop.loc[((df_1st_drop['ae_ID']!='DUMMY')&(df_1st_drop['LedgerBal']<0))]

#df_ex.info()
ex_list = df_ex['ClntCode'].unique() # type=numpy # client ID swing from int64 or obj <- depend C209868 if exist(obj) else(int64) <- try make it must obj becoz df hv all a/c must obj

## new add get client list if from internet
ex_internet = df_ex.loc[df_ex['Source'] == 'Internet', 'ClntCode'] # type = pandas
ex_internet=ex_internet.values.tolist() # change df into list
##

#print(ex_list) # must be [] of string for later use # but here is numpy is still ok 
df_1st_drop_ex = df_1st_drop[df_1st_drop['ClientID'].isin(ex_list)]

### add from internet column
condition = df_1st_drop_ex['ClientID'].isin(ex_internet) # type = pandas
df_1st_drop_ex = pd.concat([df_1st_drop_ex, condition], axis=1, join='inner')
df_1st_drop_ex.columns = ['ClientID', 'TradingACCSEQ', 'Name', 'ae_ID', 'INVDESC', 'CCY', 'On_Hand', 'non_settle_trade', 'LedgerBal', 'Hold', 'Reserve', 'Internet']
#df_1st_drop_ex = df_1st_drop_ex.assign(Source=lambda x: True if condition.any() else False)
###

df_1st_drop_not = df_1st_drop[~df_1st_drop['ClientID'].isin(ex_list)]

#df_short = df_1st_drop_not.loc[(~(df_1st_drop_not['ae_ID'].isin(['DUMMY','ED02','9999RST','ED01RST']))&((df_1st_drop_not['Settle+Due']<0)|(df_1st_drop_not['LedgerBal']<0)))]
df_short = df_1st_drop_not.loc[(~(df_1st_drop_not['ae_ID'].isin(['DUMMY','ED02','9999RST','ED01RST']))&(df_1st_drop_not['On_Hand']<0)&~(df_1st_drop_not['ClientID'].isin(['C209868'])))] # may be solely depend on 'LedgerBal<0'
short_list = df_short['ClientID'].unique()
df_short = df_1st_drop[df_1st_drop['ClientID'].isin(short_list)]

## take out single ID and with HKD only
id_counts = df_short['ClientID'].value_counts()
single_id = id_counts[id_counts == 1].index
mask = (df_short['ClientID'].isin(single_id))&(df_short['CCY']=='HKD')
df_short=df_short[~mask]

#df_1st_drop.to_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\FOCCP_'+ x +'_'+ y +'_1stdrop.csv', encoding='utf-8', index=False)
df_1st_drop_ex.to_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\tests\\tests_result\\FOCCP_'+ x +'_ex.csv', encoding='utf-8', index=False)
df_short.to_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\tests\\tests_result\\FOCCP_'+ x +'_not_ex.csv', encoding='utf-8', index=False)

# df : raw 
# df_ex : conversion real transaction
# df_1st_drop : df -> cut off unnessary column
# df_short : df_1st_drop -> filter out ['DUMMY','ED02','9999RST','ED01RST'] and ('LedgerBal < 0')
# df_1st_drop_ex : df_1st_drop -> only real conversion client list
# df_1st_drop_not : df_1st_drop -> non real converson client list

