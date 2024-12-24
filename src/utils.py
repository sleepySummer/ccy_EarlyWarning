#import csv

class Common_Utils:
    @staticmethod
    def select_date_and_session():
        x = input('Date(yyyymmdd):')
        y = input('am/pm:')
        return x, y

    @staticmethod
    def export_result(path,data):
        if path[-3:] == "csv":
            data.to_csv(path, encoding='utf-8', index=False)
        else:
            data.to_excel(path, index=True) 


    


