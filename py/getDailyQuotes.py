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
                not dataSheets[count + 6].isNone() and \
                not dataSheets[count + 7].isNone():
                if  dataSheets[count    ].isNegative()      and CommonPackage.isDesc(dataSheets[count    ],dataSheets[count + 1]) and \
                    dataSheets[count + 1].isNegative()      and CommonPackage.isDesc(dataSheets[count + 1],dataSheets[count + 2]) and \
                    dataSheets[count + 2].isNegative()      and CommonPackage.isDesc(dataSheets[count + 2],dataSheets[count + 3]) and \
                    dataSheets[count + 4].isSmallPositive() and CommonPackage.isAsce(dataSheets[count + 3],dataSheets[count + 4]) and \
                    dataSheets[count + 5].isPositive()      and CommonPackage.isAsce(dataSheets[count + 1],dataSheets[count + 2]) and \
                    dataSheets[count + 6].isPositive()      and CommonPackage.isAsce(dataSheets[count + 2],dataSheets[count + 3]) and \
                    dataSheets[count + 7].isPositive():
                    dataSheets[count + 7].set7DaysStatus(3)
                    print(dataSheets[count + 7].get7DaysStatus().getAnzlyzedDataString())
            if count + 6 >= length:
                continue
            if  not dataSheets[count    ].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone() and \
                not dataSheets[count + 5].isNone() and \
                not dataSheets[count + 6].isNone():
                if  dataSheets[count    ].isNegative()      and CommonPackage.isDesc(dataSheets[count    ],dataSheets[count + 1]) and \
                    dataSheets[count + 1].isNegative()      and CommonPackage.isDesc(dataSheets[count + 1],dataSheets[count + 2]) and \
                    dataSheets[count + 2].isNegative()      and CommonPackage.isDesc(dataSheets[count + 2],dataSheets[count + 3]) and \
                    dataSheets[count + 4].isCross()         and CommonPackage.isAsce(dataSheets[count + 3],dataSheets[count + 4]) and \
                    CommonPackage.isAsce(dataSheets[count + 1],dataSheets[count + 2]) and \
                    CommonPackage.isAsce(dataSheets[count + 2],dataSheets[count + 3]):
                    dataSheets[count + 7].set6DaysStatus(4)
                    print(dataSheets[count + 7].get6DaysStatus().getAnzlyzedDataString())
            if count + 5 >= length:
                continue
            if  not dataSheets[count    ].isNone() and \
                not dataSheets[count + 1].isNone() and \
                not dataSheets[count + 2].isNone() and \
                not dataSheets[count + 3].isNone() and \
                not dataSheets[count + 4].isNone():
                if  dataSheets[count    ].isNegative() and CommonPackage.isDesc(dataSheets[count    ],dataSheets[count + 1]) and \
                    dataSheets[count + 1].isNegative() and CommonPackage.isDesc(dataSheets[count + 1],dataSheets[count + 2]) and \
                    dataSheets[count + 2].isNegative() and CommonPackage.isDesc(dataSheets[count + 2],dataSheets[count + 3]) and \
                    dataSheets[count + 3].isNegative() and CommonPackage.isDesc(dataSheets[count + 3],dataSheets[count + 4]):
                    dataSheets[count + 4].set5DaysStatus(0)
                    print(dataSheets[count + 4].get5DaysStatus().getAnzlyzedDataString())
                if  dataSheets[count    ].isNegative()    and CommonPackage.isDesc(dataSheets[count    ],dataSheets[count + 1]) and \
                    dataSheets[count + 1].isBigNegative() and CommonPackage.isDesc(dataSheets[count + 1],dataSheets[count + 2]) and \
                    dataSheets[count + 2].isBigNegative() and CommonPackage.isDesc(dataSheets[count + 2],dataSheets[count + 3]) and \
                    dataSheets[count + 3].isBigNegative() and CommonPackage.isDesc(dataSheets[count + 3],dataSheets[count + 4]):
                    dataSheets[count + 4].set5DaysStatus(1)
                    print(dataSheets[count + 4].get5DaysStatus().getAnzlyzedDataString())
                if  dataSheets[count    ].isNegative()      and CommonPackage.isDesc(dataSheets[count    ],dataSheets[count + 1]) and \
                    dataSheets[count + 1].isNegative()      and CommonPackage.isDesc(dataSheets[count + 1],dataSheets[count + 2]) and \
                    dataSheets[count + 2].isNegative()      and CommonPackage.isDesc(dataSheets[count + 2],dataSheets[count + 3]) and \
                    dataSheets[count + 3].isSmallPositive() and CommonPackage.isAsce(dataSheets[count + 3],dataSheets[count + 4]) and \
                    dataSheets[count + 4].isBigNegative():
                    dataSheets[count + 4].set5DaysStatus(2)
                    print(dataSheets[count + 4].get5DaysStatus().getAnzlyzedDataString())
            fill = openpyxl.styles.PatternFill(patternType='solid',fgColor='FFFFFF',bgColor='FFFFFF')                        

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
        for count, data in enumerate(dataSheets,start=2):
            data.write(worksheet,count)

    workbook.save(xlsxPath)
    workbook.close()