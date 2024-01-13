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
        dataSheets = list()
        for daily_quote in daily_quotes_json['daily_quotes']:
            dataSheets.append(Data.Data(daily_quote))
        
        length = len(dataSheets)
        for count in range(length):
            if count + 8 >= length:
                continue
            if count + 7 >= length:
                continue
            if  not dataSheets[count    ].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone() and \
                not dataSheets[count + 5].isNone() and \
                not dataSheets[count + 6].isNone():
                CommonPackage.pattern03(dataSheets,count)
                CommonPackage.pattern09(dataSheets,count)
                CommonPackage.pattern10(dataSheets,count)
                CommonPackage.pattern11(dataSheets,count)
                CommonPackage.pattern17(dataSheets,count)
                CommonPackage.pattern18(dataSheets,count)
                CommonPackage.pattern19(dataSheets,count)
                CommonPackage.pattern20(dataSheets,count)
            if count + 6 >= length:
                continue
            if  not dataSheets[count    ].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone() and \
                not dataSheets[count + 5].isNone():
                CommonPackage.pattern04(dataSheets,count)
                CommonPackage.pattern05(dataSheets,count)
                CommonPackage.pattern06(dataSheets,count)
                CommonPackage.pattern07(dataSheets,count)
                CommonPackage.pattern08(dataSheets,count)
                CommonPackage.pattern12(dataSheets,count)
                CommonPackage.pattern13(dataSheets,count)
                CommonPackage.pattern14(dataSheets,count)
                CommonPackage.pattern15(dataSheets,count)
                CommonPackage.pattern16(dataSheets,count)
                CommonPackage.pattern21(dataSheets,count)
                CommonPackage.pattern22(dataSheets,count)
                CommonPackage.pattern23(dataSheets,count)
            if count + 5 >= length:
                continue
            if  not dataSheets[count    ].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone():
                CommonPackage.pattern00(dataSheets,count)
                CommonPackage.pattern01(dataSheets,count)
                CommonPackage.pattern02(dataSheets,count)
            fill = openpyxl.styles.PatternFill(patternType='solid',fgColor='FFFFFF',bgColor='FFFFFF')                        

        worksheet = workbook.create_sheet(title=code)
        worksheet['A1']  = "Date"
        worksheet['B1']  = "Open"
        worksheet['C1']  = "High"
        worksheet['D1']  = "Low"
        worksheet['E1']  = "Close"
        worksheet['F1']  = "UpperLimit"
        worksheet['G1']  = "LowerLimit"
        worksheet['H1']  = "Volume"
        worksheet['I1']  = "TurnoverValue"
        worksheet['J1']  = "AdjustmentFactor"
        worksheet['K1']  = "AdjustmentOpen"
        worksheet['L1']  = "AdjustmentHigh"
        worksheet['M1']  = "AdjustmentLow"
        worksheet['N1']  = "AdjustmentClose"
        worksheet['O1']  = "AdjustmentVolume"
        worksheet['P1']  = "Result"
        worksheet['Q1']  = "ResultRatio"
        worksheet['R1']  = "min"
        worksheet['S1']  = "max"
        worksheet['T1']  = "Desc or Asce"
        worksheet['U1']  = "exists Window"
        worksheet['V1']  = "ResultRatio"
        worksheet['W1']  = "ResultRatio"
        worksheet['X1']  = "ResultRatio"
        worksheet['Y1']  = "ResultRatio"
        worksheet['Z1']  = "ResultRatio"
        worksheet['AA1'] = "Result5Days"
        worksheet['AB1'] = "Result6Days"
        worksheet['AC1'] = "Result7Days"
        worksheet['AD1'] = "Result8Days"

        previous = None
        for count, data in enumerate(dataSheets,start=2):
            data.write(worksheet,count)
            if previous != None:
                if CommonPackage.isDesc(previous,data):
                    worksheet[f'T{count}'] = "Desc"
                elif CommonPackage.isAsce(previous,data):
                    worksheet[f'T{count}'] = "Asce"
                else:
                    worksheet[f'T{count}'] = "Flat"
                if CommonPackage.existsWindow(previous,data):
                    worksheet[f'U{count}'] = "Window"
            previous = data

    workbook.save(xlsxPath)
    workbook.close()