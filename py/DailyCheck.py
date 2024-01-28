import CommonPackage
import Period
import Token
import Brand
import DailyJpxData
import TradingCalender
import BrandJpxData
import os
import math
import json
import requests
import glob
import datetime
import openpyxl

from multiprocessing import Process

refreshToken, idToken = Token.getTokens()

def dailyCheck(idToken,brandData,distance=0):

    headers = {'Authorization': f'Bearer {idToken}'}
    brandCode = brandData.getCode()
    currentPath = CommonPackage.createDir(os.path.join(CommonPackage.dataDir,brandData.getCode()))

    if distance == -1:
        dailyQuotesGet = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={brandCode}", headers=headers)
    else:
        date = Period.Period.getDate(distance).strftime('%Y-%m-%d')
        dailyQuotesGet = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={brandCode}&date={date}", headers=headers)

    dailyQuotesJson = dailyQuotesGet.json()

    if 'daily_quotes' in dailyQuotesJson and len(dailyQuotesJson['daily_quotes'])!=0:
        for dailyQuote in dailyQuotesJson['daily_quotes']:
            current = dailyQuote['Date']
            currentFilePath = os.path.join(currentPath,current+".json")
            if not os.path.exists(currentFilePath):
                with open(currentFilePath, 'w') as f:
                    json.dump(dailyQuote, f)

def readDailyAllJpxData(brandData):

    allDailyJpxDataList = list()
    for i,bd in enumerate(brandData):
        if i > 1:
            break
        currentPath = os.path.join(CommonPackage.dataDir,bd.getCode())
        fileList = sorted(glob.glob(currentPath+'/*.json',recursive=False))
        dailyJpxDataList = list()
        for j,fl in enumerate(fileList,2):
            with open(fl) as f:
                dailyJpxData = DailyJpxData.DailyJpxData(json.load(f))
            dailyJpxDataList.append(dailyJpxData)
        allDailyJpxDataList.append(BrandJpxData.BrandJpxData(bd,dailyJpxDataList))
    return allDailyJpxDataList


def writeDailyXlsx(allDailyJpxDataList):
    xlsxPath = os.path.join(CommonPackage.dataDir,datetime.datetime.today().strftime('%Y-%m-%d')+"-daily.xlsx")

    workbook = openpyxl.Workbook()
    worksheet = workbook.get_sheet_by_name('Sheet')
    workbook.remove(worksheet)
    print(xlsxPath)

    for i,adjdl in enumerate(allDailyJpxDataList):
        if i>1:
            break
        worksheet = workbook.create_sheet(title=adjdl.getBrandCode())
        DailyJpxData.DailyJpxData.writeJpxHeader(worksheet,1)
        noneCount = 0
        for j,jdl in enumerate(adjdl.getJpxDataList(),2):
             if not jdl.writeJpxData(worksheet,j-noneCount):
                 noneCount += 1
    workbook.save(xlsxPath)
    workbook.close()          


if __name__ == '__main__':

    brandData = [Brand.BrandData(info) for info in Brand.BrandData.getBrandInfo(idToken)]
    tradingCalender = TradingCalender.TradingCalender(idToken)

    length = len(brandData)
    for iter in range(math.ceil(length/CommonPackage.numOfThreads)):
        process = list()
        nextIter = CommonPackage.getNextInterIter(length,iter,CommonPackage.numOfThreads)
        for thread in range(nextIter):
            break
            process.append(Process(target=dailyCheck,args=(idToken,brandData[iter*CommonPackage.numOfThreads+thread],1)))
        for p in process:
            p.start()
        for p in process:
            p.join()

    allDailyJpxData = readDailyAllJpxData(brandData)

    writeDailyXlsx(allDailyJpxData)