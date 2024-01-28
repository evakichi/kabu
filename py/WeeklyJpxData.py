import Quotes
import CandleStick
import Combination
import sys

class WeeklyJpxData():

    yearWeek         = None
    quotes           = None
    quotesList       = None
    candleStick = None
    combination = None

    def __init__(self,yearWeek,weeklyJpxData) -> None:

        self.yearWeek          = yearWeek
        
        self.quotesList=list()
        self.quotesList.append(weeklyJpxData.quotes)

    def append(self,weeklyJpxData):
        self.quotesList.append(weeklyJpxData.quotes)

    def reCalc(self,prev):
        open = self.quotesList[0].open
        high = -sys.float_info.max
        low  = sys.float_info.max
        for ql in self.quotesList:
            high = max(ql.high,high)
            low  = min(ql.low,low)
        close = self.quotesList[-1].close
        self.quotes = Quotes.Quotes(open,high,low,close)
        self.candleStick = CandleStick.CandleStick(self.quotes)
        self.combination = Combination.Combination(prev,self)

    def print(self):
        print(f'{self.yearWeek}:{self.quotes.open}-{self.quotes.high}-{self.quotes.low}-{self.quotes.close}')
    
    def writeJpxHeader(worksheet,count):
        worksheet[f'A{count}']  = 'yearWeek'
        worksheet[f'B{count}']  = 'open'
        worksheet[f'C{count}']  = 'high'
        worksheet[f'D{count}']  = 'low'
        worksheet[f'E{count}']  = 'close'
        worksheet[f'F{count}']  = 'threeTypeCandleStick'
        worksheet[f'G{count}']  = 'nineTypeCandleStick'
        worksheet[f'H{count}']  = 'fifteenTypeCandleStick'
        worksheet[f'L{count}']  = 'combination'

    def writeJpxData(self,worksheet,count):
        if self.yearWeek == None:
            return False
        worksheet[f'A{count}']  = self.yearWeek
        worksheet[f'B{count}']  = self.quotes.open
        worksheet[f'C{count}']  = self.quotes.high
        worksheet[f'D{count}']  = self.quotes.low
        worksheet[f'E{count}']  = self.quotes.close
        if self.candleStick != None:
            worksheet[f'F{count}']  = self.candleStick.getThreeTypeString()
            worksheet[f'G{count}']  = self.candleStick.getNineTypeString()
            worksheet[f'H{count}']  = self.candleStick.getSeventeenTypeString()
            worksheet[f'I{count}']  = CandleStick.CandleStick.calcOpenCloseRatio(self.quotes.open,self.quotes.close)
            worksheet[f'J{count}']  = CandleStick.CandleStick.calcLowBeardRatio(self.quotes.open,self.quotes.high,self.quotes.low,self.quotes.close)
            worksheet[f'K{count}']  = CandleStick.CandleStick.calcHighBeardRatio(self.quotes.open,self.quotes.high,self.quotes.low,self.quotes.close)
        if self.combination != None and self.combination.combinationType != None:
            worksheet[f'L{count}']  = self.combination.combinationType.getString()

        return True        
