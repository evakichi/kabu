import CommonPackage
import requests
import Brand
import Period
import TradingCalender
import os
import json

class JpxData:

    date             = None
    open             = 0.0
    high             = 0.0
    low              = 0.0
    close            = 0.0
    upperLimit       = 0
    lowerLimit       = 0
    volume           = 0
    turnoverValue    = 0.0
    adjustmentFactor = 0.0
    adjustmentOpen   = 0.0
    adjustmentHigh   = 0.0
    adjustmentLow    = 0.0
    adjustmentClose  = 0.0
    adjustmentVolume = 0

    def __init__(self,data) -> None:
        if data == None:
            return None
        
        if data['Open'] == None or data['High'] == None or data['Low'] == None or data['Close'] == None:
            self.isNoneValue = True
            return None
        self.date              = data['Date']
        self.open              = float(data['Open'])
        self.high              = float(data['High'])
        self.low               = float(data['Low'])
        self.close             = float(data['Close'])
        self.upperLimit        = int(data['UpperLimit'])
        self.lowerLimit        = int(data['LowerLimit'])
        self.volume            = int(data['Volume'])
        self.turnoverValue     = float(data['TurnoverValue'])
        self.adjustmentFactor  = float(data['AdjustmentFactor'])
        self.adjustmentOpen    = float(data['AdjustmentOpen'])
        self.adjustmentHigh    = float(data['AdjustmentHigh'])
        self.adjustmentLow     = float(data['AdjustmentLow'])
        self.adjustmentClose   = float(data['AdjustmentClose'])
        self.adjustmentVolume  = int(data['AdjustmentVolume'])

    def getDailyJpxData(idToken,brandData,path,distance):
        headers = {'Authorization': f'Bearer {idToken}'}
        brandCode = brandData.getCode()
        current = Period.Period.getDate(distance).strftime('%Y-%m-%d')

        dailyQuotesGet = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={brandCode}&date={current}", headers=headers)
        dailyQuotesJson = dailyQuotesGet.json()

        #print(brandCode,tradingCalender.isBusinessDay(current),dailyQuotesJson)
        if len(dailyQuotesJson['daily_quotes'])!=0:
         #   print(dailyQuotesJson['daily_quotes'])
            dailyQuote = dailyQuotesJson['daily_quotes'][0]
            with open(os.path.join(path,current+".json"), 'w') as f:
               json.dump(dailyQuote, f)
