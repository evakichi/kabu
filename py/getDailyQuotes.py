import CommonPackage
import os
import requests
import openpyxl
from multiprocessing import Process,Queue

def getDataAndWriteXslx(code,fromDate,toDate,headers,queue):
    queue.put((code,daily_quotes_json))

if __name__ == '__main__':
    numOfThreads = 20 
    home = os.environ.get('HOME')
    refreshToken, idToken = CommonPackage.getTokens()
    fromDate,toDate = CommonPackage.getDates()

    path = CommonPackage.createDir(os.path.join(home,"daily_quotes/"))
    period = f"{fromDate}-{toDate}"
    xlsxPath = os.path.join(home,"daily_quotes/",period+".xlsx")

    workbook = openpyxl.Workbook()
    worksheet = workbook.get_sheet_by_name('Sheet')
    workbook.remove(worksheet)
    print(xlsxPath)

    information = CommonPackage.getBrandInfo(idToken)
    headers = {'Authorization': f'Bearer {idToken}'}
    for infoCount,info in enumerate(information):
        code = info['Code']
        print(f'{infoCount}:{code}')
        daily_quotes_get = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={code}&from={fromDate}&to={toDate}", headers=headers)
        daily_quotes_json = daily_quotes_get.json()
        worksheet = workbook.create_sheet(title=code)
        worksheet['A1']="Date"
        worksheet['B1']="Open"
        worksheet['C1']="High"
        worksheet['D1']="Low"
        worksheet['E1']="Close"
        worksheet['F1']="UpperLimit"
        worksheet['G1']="LowerLimit"
        worksheet['H1']="Volume"
        worksheet['I1']="TurnoverValue"
        worksheet['J1']="AdjustmentFactor"
        worksheet['K1']="AdjustmentOpen"
        worksheet['L1']="AdjustmentHigh"
        worksheet['M1']="AdjustmentLow"
        worksheet['N1']="AdjustmentClose"
        worksheet['O1']="AdjustmentVolume"

        for quoteCount,daily_quote in enumerate(daily_quotes_json['daily_quotes'],start=2):
            worksheet[f"A{quoteCount}"] = daily_quote['Date']
            worksheet[f"B{quoteCount}"] = daily_quote['Open']
            worksheet[f"C{quoteCount}"] = daily_quote['High']
            worksheet[f"D{quoteCount}"] = daily_quote['Low']
            worksheet[f"E{quoteCount}"] = daily_quote['Close']
            worksheet[f"F{quoteCount}"] = daily_quote['UpperLimit']
            worksheet[f"G{quoteCount}"] = daily_quote['LowerLimit']
            worksheet[f"H{quoteCount}"] = daily_quote['Volume']
            worksheet[f"I{quoteCount}"] = daily_quote['TurnoverValue']
            worksheet[f"J{quoteCount}"] = daily_quote['AdjustmentFactor']
            worksheet[f"K{quoteCount}"] = daily_quote['AdjustmentOpen']
            worksheet[f"L{quoteCount}"] = daily_quote['AdjustmentHigh']
            worksheet[f"M{quoteCount}"] = daily_quote['AdjustmentLow']
            worksheet[f"N{quoteCount}"] = daily_quote['AdjustmentClose']
            worksheet[f"O{quoteCount}"] = daily_quote['AdjustmentVolume']

    workbook.save(xlsxPath)
    workbook.close()