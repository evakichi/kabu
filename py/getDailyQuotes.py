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
#        if infoCount >= 20:
#            break
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
            if  not dataSheets[count + 0].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone() and \
                not dataSheets[count + 5].isNone() and \
                not dataSheets[count + 6].isNone() and \
                not dataSheets[count + 7].isNone():
                CommonPackage.pattern3200(dataSheets,count)
                CommonPackage.pattern4100(dataSheets,count)
                CommonPackage.pattern4200(dataSheets,count)
                CommonPackage.pattern4300(dataSheets,count)
                CommonPackage.pattern4403(dataSheets,count)
            if count + 7 >= length:
                continue
            if  not dataSheets[count + 0].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone() and \
                not dataSheets[count + 5].isNone() and \
                not dataSheets[count + 6].isNone():
                CommonPackage.pattern0300(dataSheets,count)
                CommonPackage.pattern0900(dataSheets,count)
                CommonPackage.pattern1000(dataSheets,count)
                CommonPackage.pattern1100(dataSheets,count)
                CommonPackage.pattern1700(dataSheets,count)
                CommonPackage.pattern1800(dataSheets,count)
                CommonPackage.pattern1900(dataSheets,count)
                CommonPackage.pattern2000(dataSheets,count)
                CommonPackage.pattern2000(dataSheets,count)
                CommonPackage.pattern2700(dataSheets,count)
                CommonPackage.pattern2800(dataSheets,count)
                CommonPackage.pattern3000(dataSheets,count)
                CommonPackage.pattern3302(dataSheets,count)
                CommonPackage.pattern4402(dataSheets,count)
            if count + 6 >= length:
                continue
            if  not dataSheets[count + 0].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone() and \
                not dataSheets[count + 5].isNone():
                CommonPackage.pattern0400(dataSheets,count)
                CommonPackage.pattern0500(dataSheets,count)
                CommonPackage.pattern0600(dataSheets,count)
                CommonPackage.pattern0700(dataSheets,count)
                CommonPackage.pattern0800(dataSheets,count)
                CommonPackage.pattern1200(dataSheets,count)
                CommonPackage.pattern1300(dataSheets,count)
                CommonPackage.pattern1400(dataSheets,count)
                CommonPackage.pattern1500(dataSheets,count)
                CommonPackage.pattern1600(dataSheets,count)
                CommonPackage.pattern2100(dataSheets,count)
                CommonPackage.pattern2200(dataSheets,count)
                CommonPackage.pattern2300(dataSheets,count)
                CommonPackage.pattern2400(dataSheets,count)
                CommonPackage.pattern2500(dataSheets,count)
                CommonPackage.pattern2600(dataSheets,count)
                CommonPackage.pattern3000(dataSheets,count)
                CommonPackage.pattern3301(dataSheets,count)
                CommonPackage.pattern3400(dataSheets,count)
                CommonPackage.pattern3500(dataSheets,count)
                CommonPackage.pattern3600(dataSheets,count)
                CommonPackage.pattern3700(dataSheets,count)
                CommonPackage.pattern3800(dataSheets,count)
                CommonPackage.pattern3900(dataSheets,count)
                CommonPackage.pattern4401(dataSheets,count)
            if count + 5 >= length:
                continue
            if  not dataSheets[count + 0].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone():
                CommonPackage.pattern0000(dataSheets,count)
                CommonPackage.pattern0100(dataSheets,count)
                CommonPackage.pattern0200(dataSheets,count)
                CommonPackage.pattern3100(dataSheets,count)
                CommonPackage.pattern4400(dataSheets,count)
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