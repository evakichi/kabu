import CommonPackage
import os
import requests
import openpyxl
import math
from multiprocessing import Process,Queue
import Data

if __name__ == '__main__':
    numOfThreads = 20 
    home = os.environ.get('HOME')
    refreshToken, idToken = CommonPackage.getTokens()
    fromDate,toDate = CommonPackage.getDates(730,84)

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
        if infoCount >= 20:
            break
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
        worksheet['P1']="Result"
        worksheet['Q1']="ResultRatio"
        worksheet['R1']="Result5Days"
        worksheet['S1']="Result6Days"
        worksheet['T1']="Result7Days"
        worksheet['U1']="Result8Days"

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

        for count in range()
            current = Data.Data(daily_quote['Open'],daily_quote['High'],daily_quote['Low'],daily_quote['Close'])
            if current.isNone:
                continue
            fill = openpyxl.styles.PatternFill(patternType='solid',fgColor='FFFFFF',bgColor='FFFFFF')                        
            dailyResult = ""
            result4Days = ""
            result5Days = ""
            result6Days = ""
            result7Days = ""
            result8Days = ""
            worksheet[f"P{quoteCount}"] = current.getCandleState()
            worksheet[f"P{quoteCount}"].fill = fill
            worksheet[f"Q{quoteCount}"] = current.getRatio()
            worksheet[f"Q{quoteCount}"].fill = fill
            if quoteCount > 10:
                pastDays= CommonPackage.getPastDays(worksheet,quoteCount,8)
                if  not pastDays[-5].isNone() and \
                    not pastDays[-4].isNone() and \
                    not pastDays[-3].isNone() and \
                    not pastDays[-2].isNone() and \
                    not pastDays[-1].isNone():
                    if  pastDays[-5].isNegative() and CommonPackage.isDesc(pastDays[-5],pastDays[-4]) and \
                        pastDays[-4].isNegative() and CommonPackage.isDesc(pastDays[-4],pastDays[-3]) and \
                        pastDays[-3].isNegative() and CommonPackage.isDesc(pastDays[-3],pastDays[-2]) and \
                        pastDays[-2].isNegative() and CommonPackage.isAsce(pastDays[-2],pastDays[-1]):
                        result5Days = "三空叩き込み"
                        print("三空叩き込み")
                    if  pastDays[-5].isNegative() and CommonPackage.isDesc(pastDays[-5],pastDays[-4]) and \
                        pastDays[-4].isBigNegative() and CommonPackage.isDesc(pastDays[-4],pastDays[-3]) and \
                        pastDays[-3].isBigNegative() and CommonPackage.isDesc(pastDays[-3],pastDays[-2]) and \
                        pastDays[-2].isBigNegative() and CommonPackage.isDesc(pastDays[-2],pastDays[-1]):
                        result5Days = "三手大陰線"
                        print("三手大陰線")
                    if  pastDays[-5].isNegative() and CommonPackage.isDesc(pastDays[-5],pastDays[-4]) and \
                        pastDays[-4].isBigNegative() and CommonPackage.isDesc(pastDays[-4],pastDays[-3]) and \
                        pastDays[-3].isBigNegative() and CommonPackage.isDesc(pastDays[-3],pastDays[-2]) and \
                        pastDays[-2].isBigNegative() and CommonPackage.isDesc(pastDays[-2],pastDays[-1]):
                        result5Days = "三手大陰線"
                        print("三手大陰線")
            worksheet[f"R{quoteCount}"] = result5Days
            worksheet[f"S{quoteCount}"] = result6Days
            worksheet[f"T{quoteCount}"] = result7Days
            worksheet[f"U{quoteCount}"] = result8Days

    workbook.save(xlsxPath)
    workbook.close()