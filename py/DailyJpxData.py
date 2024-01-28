import JpxData
import CandleStick

class DailyJpxData(JpxData.JpxData):

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
    candleStick = None


    def __init__(self,jsonData) -> None:
        if jsonData == None:
            return None
        
        if jsonData['Open'] == None or jsonData['High'] == None or jsonData['Low'] == None or jsonData['Close'] == None:
            self.isNoneValue = True
            return None
        self.date              = jsonData['Date']
        super().__init__(float(jsonData['Open']),float(jsonData['High']),float(jsonData['Low']),float(jsonData['Close']))
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

        self.candleStick = CandleStick.CandleStick(self.open,self.high,self.low,self.close)

    def print(self):
        print(f'{self.date}:{self.open}-{self.high}-{self.low}-{self.close}')

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

    def writeJpxData(self,worksheet,count):
        worksheet[f'A{count}']  = self.date
        worksheet[f'B{count}']  = self.open
        worksheet[f'C{count}']  = self.high
        worksheet[f'D{count}']  = self.low
        worksheet[f'E{count}']  = self.close
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
            worksheet[f'R{count}']  = self.candleStick.getFifteenTypeString()
            worksheet[f'S{count}']  = CandleStick.CandleStick.calcOpenCloseRatio(self.open,self.close)
            worksheet[f'T{count}']  = CandleStick.CandleStick.calcLowBeardRatio(self.open,self.high,self.low,self.close)
            worksheet[f'U{count}']  = CandleStick.CandleStick.calcHighBeardRatio(self.open,self.high,self.low,self.close)
        
