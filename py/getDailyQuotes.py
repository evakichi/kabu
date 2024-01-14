import CommonPackage
import os
import requests
import openpyxl
import math
from multiprocessing import Process,Queue
import Data

def loadAndCalc(code,fromDate,toDate,headers,count,queue,debug):
    print(f'{count}:{code}')
    
    daily_quotes_get = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={code}&from={fromDate}&to={toDate}", headers=headers)
    daily_quotes_json = daily_quotes_get.json()

    datasheet = list()
    for daily_quote in daily_quotes_json['daily_quotes']:
        data = Data.Data(daily_quote,0.05,0.05)
        if not data.isNone():
            datasheet.append(data)
    length = len(datasheet)
    previous = None
    for counter in range(length):
        current = datasheet[counter]
        if previous != None:
            current.setFactor(previous)
#            if debug:
#                current.printFactors()
        if counter + 8 >= length:
            continue
        CommonPackage.pattern3200(datasheet,counter,debug)
        CommonPackage.pattern4100(datasheet,counter,debug)
        CommonPackage.pattern4200(datasheet,counter,debug)
        CommonPackage.pattern4300(datasheet,counter,debug)
        CommonPackage.pattern4403(datasheet,counter,debug)
        if counter + 7 >= length:
            continue
        CommonPackage.pattern0300(datasheet,counter,debug)
        CommonPackage.pattern0900(datasheet,counter,debug)
        CommonPackage.pattern1000(datasheet,counter,debug)
        CommonPackage.pattern1100(datasheet,counter,debug)
        CommonPackage.pattern1700(datasheet,counter,debug)
        CommonPackage.pattern1800(datasheet,counter,debug)
        CommonPackage.pattern1900(datasheet,counter,debug)
        CommonPackage.pattern2000(datasheet,counter,debug)
        CommonPackage.pattern2000(datasheet,counter,debug)
        CommonPackage.pattern2700(datasheet,counter,debug)
        CommonPackage.pattern2800(datasheet,counter,debug)
        CommonPackage.pattern3000(datasheet,counter,debug)
        CommonPackage.pattern3302(datasheet,counter,debug)
        CommonPackage.pattern4402(datasheet,counter,debug)
        if counter + 6 >= length:
            continue
        CommonPackage.pattern0400(datasheet,counter,debug)
        CommonPackage.pattern0500(datasheet,counter,debug)
        CommonPackage.pattern0600(datasheet,counter,debug)
        CommonPackage.pattern0700(datasheet,counter,debug)
        CommonPackage.pattern0800(datasheet,counter,debug)
        CommonPackage.pattern1200(datasheet,counter,debug)
        CommonPackage.pattern1300(datasheet,counter,debug)
        CommonPackage.pattern1400(datasheet,counter,debug)
        CommonPackage.pattern1500(datasheet,counter,debug)
        CommonPackage.pattern1600(datasheet,counter,debug)
        CommonPackage.pattern2100(datasheet,counter,debug)
        CommonPackage.pattern2200(datasheet,counter,debug)
        CommonPackage.pattern2300(datasheet,counter,debug)
        CommonPackage.pattern2400(datasheet,counter,debug)
        CommonPackage.pattern2500(datasheet,counter,debug)
        CommonPackage.pattern2600(datasheet,counter,debug)
        CommonPackage.pattern3000(datasheet,counter,debug)
        CommonPackage.pattern3301(datasheet,counter,debug)
        CommonPackage.pattern3400(datasheet,counter,debug)
        CommonPackage.pattern3500(datasheet,counter,debug)
        CommonPackage.pattern3600(datasheet,counter,debug)
        CommonPackage.pattern3700(datasheet,counter,debug)
        CommonPackage.pattern3800(datasheet,counter,debug)
        CommonPackage.pattern3900(datasheet,counter,debug)
        CommonPackage.pattern4401(datasheet,counter,debug)
        if counter + 5 >= length:
            continue
        CommonPackage.pattern0000(datasheet,counter,debug)
        CommonPackage.pattern0100(datasheet,counter,debug)
        CommonPackage.pattern0200(datasheet,counter,debug)
        CommonPackage.pattern3100(datasheet,counter,debug)
        CommonPackage.pattern4400(datasheet,counter,debug)
        if counter + 2 >= length:
            continue
        previous = datasheet[counter]
    queue.put((code,datasheet))

if __name__ == '__main__':
    numOfThreads = 1

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
    datasheets = list()
    length = len(information)
    length = 10
    for iter in range(math.ceil(length/numOfThreads)):
        process = list()
        queue = list()
        nextIter = CommonPackage.getNextInterIter(length,iter,numOfThreads)
        for thread in range(nextIter):
            queue.append(Queue())
        for thread in range(nextIter):
            process.append(Process(target=loadAndCalc,args=(information[iter*numOfThreads+thread]['Code'],fromDate,toDate,headers,iter*numOfThreads+thread,queue[thread],True)))
        for thread in range(nextIter):
            process[thread].start()
        for q in queue:
            datasheets.append(q.get())
        for thread in range(nextIter):
            process[thread].join()
    for data in datasheets:
        code,sheets = data
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
        worksheet['P1']  = "CandleState"
        worksheet['Q1']  = "Factor"
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

        for count, data in enumerate(sheets,start=2):
            data.write(worksheet,count)

    workbook.save(xlsxPath)
    workbook.close()