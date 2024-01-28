import Quotes
import CandleStick
import Combination

class JpxData:

    date             = None
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

    def __init__(self) -> None:
        pass

class DailyJpxData():

    date             = None
    quotes           = None
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
    candleStick = None
    combination = None

    isNone = False


    def __init__(self,jsonData,prev) -> None:

        if jsonData == None:
            return 
        
        if jsonData['Open'] == None or jsonData['High'] == None or jsonData['Low'] == None or jsonData['Close'] == None:
            return 

        self.date              = jsonData['Date']
        
        open  = float(jsonData['Open'])
        high  = float(jsonData['High'])
        low   = float(jsonData['Low'])
        close = float(jsonData['Close'])

        self.quotes            = Quotes.Quotes(open,high,low,close)

        self.upperLimit        = int(jsonData['UpperLimit'])
        self.lowerLimit        = int(jsonData['LowerLimit'])
        self.volume            = int(jsonData['Volume'])
        self.turnoverValue     = float(jsonData['TurnoverValue'])
        self.adjustmentFactor  = float(jsonData['AdjustmentFactor'])
        self.adjustmentOpen    = float(jsonData['AdjustmentOpen'])
        self.adjustmentHigh    = float(jsonData['AdjustmentHigh'])
        self.adjustmentLow     = float(jsonData['AdjustmentLow'])
        self.adjustmentClose   = float(jsonData['AdjustmentClose'])
        self.adjustmentVolume  = int(jsonData['AdjustmentVolume'])

        self.candleStick = CandleStick.CandleStick(self.quotes)
        self.combination = Combination.Combination(prev,self)

    def print(self):
        print(f'{self.date}:{self.quotes.open}-{self.quotes.high}-{self.quotes.low}-{self.quotes.close}')

    def getQuotes(self):
        return self.quotes
    
    def isNoneValue(self):
        return self.isNone

    def getCandleStick(self):
        return self.candleStick
    
    def getCombination(self):
        return self.combination
    
    def writeJpxHeader(worksheet,count):
        worksheet[f'A{count}']  = 'date'
        worksheet[f'B{count}']  = 'open'
        worksheet[f'C{count}']  = 'high'
        worksheet[f'D{count}']  = 'low'
        worksheet[f'E{count}']  = 'close'
        worksheet[f'F{count}']  = 'upperLimit'
        worksheet[f'G{count}']  = 'lowerLimit'
        worksheet[f'H{count}']  = 'volume'
        worksheet[f'I{count}']  = 'turnoverValue'
        worksheet[f'J{count}']  = 'adjustmentFactor'
        worksheet[f'K{count}']  = 'adjustmentOpen'
        worksheet[f'L{count}']  = 'adjustmentHigh'
        worksheet[f'M{count}']  = 'adjustmentLow'
        worksheet[f'N{count}']  = 'adjustmentClose'
        worksheet[f'O{count}']  = 'adjustmentVolume'
        worksheet[f'P{count}']  = 'threeTypeCandleStick'
        worksheet[f'Q{count}']  = 'nineTypeCandleStick'
        worksheet[f'R{count}']  = 'fifteenTypeCandleStick'
        worksheet[f'V{count}']  = 'combination'

    def writeJpxData(self,worksheet,count):
        if self.date == None:
            return False
        worksheet[f'A{count}']  = self.date
        worksheet[f'B{count}']  = self.quotes.open
        worksheet[f'C{count}']  = self.quotes.high
        worksheet[f'D{count}']  = self.quotes.low
        worksheet[f'E{count}']  = self.quotes.close
        worksheet[f'F{count}']  = self.upperLimit
        worksheet[f'G{count}']  = self.lowerLimit
        worksheet[f'H{count}']  = self.volume
        worksheet[f'I{count}']  = self.turnoverValue
        worksheet[f'J{count}']  = self.adjustmentFactor
        worksheet[f'K{count}']  = self.adjustmentOpen
        worksheet[f'L{count}']  = self.adjustmentHigh
        worksheet[f'M{count}']  = self.adjustmentLow
        worksheet[f'N{count}']  = self.adjustmentClose
        worksheet[f'O{count}']  = self.adjustmentVolume
        if self.candleStick != None:
            worksheet[f'P{count}']  = self.candleStick.getThreeTypeString()
            worksheet[f'Q{count}']  = self.candleStick.getNineTypeString()
            worksheet[f'R{count}']  = self.candleStick.getSeventeenTypeString()
            worksheet[f'S{count}']  = CandleStick.CandleStick.calcOpenCloseRatio(self.quotes.open,self.quotes.close)
            worksheet[f'T{count}']  = CandleStick.CandleStick.calcLowBeardRatio(self.quotes.open,self.quotes.high,self.quotes.low,self.quotes.close)
            worksheet[f'U{count}']  = CandleStick.CandleStick.calcHighBeardRatio(self.quotes.open,self.quotes.high,self.quotes.low,self.quotes.close)
        if self.combination != None and self.combination.getCombinationType() != None:
            worksheet[f'V{count}']  = self.combination.getCombinationType().getString()

        return True        
