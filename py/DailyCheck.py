import CommonPackage
import Period
import Token
import Brand
import JpxData
import TradingCalender
import os
import math
import json
import requests
from multiprocessing import Process

refreshToken, idToken = Token.getTokens()

def getDailyJpxData(idToken,brandData,distance=0):

    headers = {'Authorization': f'Bearer {idToken}'}
    brandCode = brandData.getCode()
    path = CommonPackage.createDir(os.path.join(CommonPackage.dataDir,brandData.getCode()))

    if distance == -1:
        dailyQuotesGet = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={brandCode}", headers=headers)
    else:
        date = Period.Period.getDate(distance).strftime('%Y-%m-%d')
        dailyQuotesGet = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={brandCode}&date={date}", headers=headers)

    dailyQuotesJson = dailyQuotesGet.json()

    if 'daily_quotes' in dailyQuotesJson and len(dailyQuotesJson['daily_quotes'])!=0:
        for dailyQuote in dailyQuotesJson['daily_quotes']:
            current = dailyQuote['Date']
            currentPath = os.path.join(path,current+".json")
            if not os.path.exists(currentPath):
                with open(currentPath, 'w') as f:
                    json.dump(dailyQuote, f)

if __name__ == '__main__':

    brandData = [Brand.BrandData(info) for info in Brand.BrandData.getBrandInfo(idToken)]
    tradingCalender = TradingCalender.TradingCalender(idToken)

    length = len(brandData)
    for iter in range(math.ceil(length/CommonPackage.numOfThreads)):
        process = list()
        nextIter = CommonPackage.getNextInterIter(length,iter,CommonPackage.numOfThreads)
        for thread in range(nextIter):
            process.append(Process(target=getDailyJpxData,args=(idToken,brandData[iter*CommonPackage.numOfThreads+thread],1)))
        for thread in range(nextIter):
            process[thread].start()
        for thread in range(nextIter):
            process[thread].join()
