import CommonPackage
import os
import requests
import openpyxl
import math
from multiprocessing import Process,Queue

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
        worksheet['R1']="Result4Days"
        worksheet['S1']="Result5Days"
        worksheet['T1']="Result6Days"
        worksheet['U1']="Result7Days"
        worksheet['V1']="Result8Days"

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
            if daily_quote['Open'] != None and daily_quote['High'] != None and daily_quote['Low'] != None and daily_quote['Close'] != None:
                open  = int(daily_quote['Open'])
                high  = int(daily_quote['High'])
                low   = int(daily_quote['Low'])
                close = int(daily_quote['Close'])
                fill = openpyxl.styles.PatternFill(patternType='solid',fgColor='FFFFFF',bgColor='FFFFFF')                        
                dailyResult = ""
                result4Days = ""
                result5Days = ""
                result6Days = ""
                result7Days = ""
                result8Days = ""
                if CommonPackage.isSmallNegative(open,high,low,close):
                    dailyResult="小陰線"
                if CommonPackage.isBigNegative(open,high,low,close):
                    dailyResult="大陰線"
                if CommonPackage.isSmallPosoitive(open,high,low,close):
                    dailyResult="小陽線"
                if CommonPackage.isBigPosoitive(open,high,low,close):
                    dailyResult="大陽線"
                if CommonPackage.isCross(open,high,low,close):
                    dailyResult = "十字線"
                worksheet[f"P{quoteCount}"] = dailyResult
                worksheet[f"P{quoteCount}"].fill = fill
                worksheet[f"Q{quoteCount}"] = CommonPackage.getRatio(open,high,low,close)
                worksheet[f"Q{quoteCount}"].fill = fill
                if quoteCount > 10:
                    pastDaysOpen,pastDaysHigh,pastDaysLow,pastDaysClose,pastDaysRatio,pastDaysAbsRatio = CommonPackage.getPastDays(worksheet,quoteCount,8)
                    if  CommonPackage.isNegative(pastDaysOpen[-5],pastDaysHigh[-5],pastDaysLow[-5],pastDaysClose[-5]) and \
                        CommonPackage.isNegative(pastDaysOpen[-4],pastDaysHigh[-4],pastDaysLow[-4],pastDaysClose[-4]) and \
                        CommonPackage.isNegative(pastDaysOpen[-3],pastDaysHigh[-3],pastDaysLow[-3],pastDaysClose[-3]) and \
                        CommonPackage.isNegative(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) and \
                        not CommonPackage.isNone(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) and \
                        not CommonPackage.isNone(pastDaysOpen[-1],pastDaysHigh[-1],pastDaysLow[-1],pastDaysClose[-1]) and \
                        CommonPackage.max(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) < CommonPackage.min(pastDaysOpen[-1],pastDaysHigh[-1],pastDaysLow[-1],pastDaysClose[-1]):
                        if  CommonPackage.isBigNegative(pastDaysOpen[-3],pastDaysHigh[-3],pastDaysLow[-3],pastDaysClose[-3]) and \
                            CommonPackage.isBigNegative(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) and \
                            CommonPackage.isBigNegative(pastDaysOpen[-1],pastDaysHigh[-1],pastDaysLow[-1],pastDaysClose[-1]):
                           result4Days = "三手大陰線"
                        else:
                           result4Days = "三空叩き込み"
                    if  CommonPackage.isNegative(pastDaysOpen[-5],pastDaysHigh[-5],pastDaysLow[-5],pastDaysClose[-5]) and \
                        CommonPackage.isNegative(pastDaysOpen[-4],pastDaysHigh[-4],pastDaysLow[-4],pastDaysClose[-4]) and \
                        CommonPackage.isNegative(pastDaysOpen[-3],pastDaysHigh[-3],pastDaysLow[-3],pastDaysClose[-3]) and \
                        CommonPackage.isPositive(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) and \
                        CommonPackage.isBigNegative(pastDaysOpen[-1],pastDaysHigh[-1],pastDaysLow[-1],pastDaysClose[-1]):
                            result5Days = "最後の抱き陰線"
                    if  CommonPackage.isNegative(pastDaysOpen[-7],pastDaysHigh[-7],pastDaysLow[-7],pastDaysClose[-5]) and \
                        CommonPackage.isNegative(pastDaysOpen[-6],pastDaysHigh[-6],pastDaysLow[-6],pastDaysClose[-6]) and \
                        CommonPackage.isNegative(pastDaysOpen[-5],pastDaysHigh[-5],pastDaysLow[-5],pastDaysClose[-5]) and \
                        CommonPackage.isPositive(pastDaysOpen[-4],pastDaysHigh[-4],pastDaysLow[-4],pastDaysClose[-4]) and \
                        not CommonPackage.isNone(pastDaysOpen[-4],pastDaysHigh[-4],pastDaysLow[-4],pastDaysClose[-4]) and \
                        not CommonPackage.isNone(pastDaysOpen[-3],pastDaysHigh[-3],pastDaysLow[-3],pastDaysClose[-3]) and \
                        not CommonPackage.isNone(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) and \
                        not CommonPackage.isNone(pastDaysOpen[-1],pastDaysHigh[-1],pastDaysLow[-1],pastDaysClose[-1]) and \
                        CommonPackage.max(pastDaysOpen[-4],pastDaysHigh[-4],pastDaysLow[-4],pastDaysClose[-4]) < CommonPackage.min(pastDaysOpen[-3],pastDaysHigh[-3],pastDaysLow[-3],pastDaysClose[-3]) and \
                        CommonPackage.max(pastDaysOpen[-3],pastDaysHigh[-3],pastDaysLow[-3],pastDaysClose[-3]) < CommonPackage.min(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) and \
                        CommonPackage.max(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) < CommonPackage.min(pastDaysOpen[-1],pastDaysHigh[-1],pastDaysLow[-1],pastDaysClose[-1]) and \
                        CommonPackage.isNegative(pastDaysOpen[-3],pastDaysHigh[-3],pastDaysLow[-3],pastDaysClose[-3]) and \
                        CommonPackage.isNegative(pastDaysOpen[-2],pastDaysHigh[-2],pastDaysLow[-2],pastDaysClose[-2]) and \
                        CommonPackage.isNegative(pastDaysOpen[-1],pastDaysHigh[-1],pastDaysLow[-1],pastDaysClose[-1]):
                            result7Days = "明けの明星"
                            print("get")
            worksheet[f"R{quoteCount}"] = result4Days
            worksheet[f"S{quoteCount}"] = result5Days
            worksheet[f"T{quoteCount}"] = result6Days
            worksheet[f"U{quoteCount}"] = result7Days
            worksheet[f"V{quoteCount}"] = result8Days

    workbook.save(xlsxPath)
    workbook.close()