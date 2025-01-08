import pandas as pd
import calendar
from config import other_ccy, review_path

def edit_source(row):

    if row['Remark'] == "WMFX":
        row['Source'] = "WMFX"
    
    if any(x in row['CCYPair'] for x in other_ccy) and row['Source'] == "ETradepro":
        row['Source'] = "otherccy"

    return row

x = input('Date(yyyymmdd):')

df = pd.read_excel('//fsn1/Company Share/FUT_FX/FX/Conversion/'+ x[:4] +'/'+ calendar.month_name[int(x[4:6])][:3] +'/FXDaily_Transactions_'+ x[2:8]+ '.xls', skiprows=2)
df['empty?'] = df['Source'].isna() # all transaction hv "Source", pick out not related row
mask = df['empty?'] == False
print(df)
df = df.loc[mask]
print(df)
df = df.drop(['empty?'], axis=1)
print(df)
df = df.apply(lambda row: edit_source(row), axis=1) 

# best for drop:
# https://sparkbyexamples.com/pandas/pandas-drop-columns-by-index/

df = df.drop(df.iloc[:, 4:31],axis = 1)
cols = [0,1,2,5,6]
df=df.drop(df.columns[cols], axis=1)

df.to_csv(review_path, encoding='utf-8', index=False)
