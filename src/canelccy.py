import pandas as pd
# create a dictionary with five fields each

df_1 = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\data\\RMR0051_20240807_b4_pm.csv')
df_2 = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\data\\RMR0051_20240808_b4_am.csv')


# Convert the dictionary into DataFrame



# Remove all columns between column index 1 to 3
#df.drop(df.iloc[:, 1:85], inplace=True, axis=1)
df_1 = df_1.iloc[:, [0,-2]]
df_2 = df_2.iloc[:, [0,-2]]


df = pd.concat([df_1, df_2]).drop_duplicates(subset='ClntCode').reset_index(drop=True) # can be a update def


df = df[df.CancelCCY == "Yes"]


df = df.iloc[:,[0]]

df['ClntCode'] = df['ClntCode'].str.replace("'", "")  # just take out "'", the Dtype is still obj in pandas class

#1 save to csv now and auto change to int
df.to_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\data\\cancelccy_list.csv', encoding='utf-8', index=False) # but write into .csv, those obj like 009000 become 9000 in .csv file

df_3 = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\TTL_api\\data\\cancelccy_list.csv')  # then read in back the .csv, 9000 become int64

ex_list = df_3['ClntCode'].unique() 

print(ex_list)

df_3.info()
