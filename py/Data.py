import sys

class CandleState:
    status = ["陽の基本形",           #0
              "大陽の基本形",         #1
              "陽の丸坊主",           #2
              "陽の大引け坊主",       #3
              "陽の寄り付き坊主",     #4
              "小陽の基本形",         #5
              "下影陽線",             #6
              "陽のコマ",             #7
              "上影陽線",             #8
              "陽のカラカサ",         #9
              "陰の基本形",           #10
              "大陰の基本形",         #11
              "陰の丸坊主",           #12
              "陽の寄り付き坊主",     #13
              "陰の大引け坊主",       #14
              "小陰の基本形",         #15
              "下影陰線",             #16
              "陰のコマ",             #17
              "上影陰線",             #18
              "陰のカラカサ",         #19
              "十字線の基本形",       #20
              "トンカチ",             #21
              "トンボ",               #22
              "足長クロス",           #23
              "トウバ",               #24
              "一本線"                #25
             ]
    
    state = -1

    def __init__(self) -> None:
        self.state = -1

    def setState(self,state):
        self.state = state

    def getState(self):
        return self.state

    def getStateString(self):
        return self.status[self.state]

class AnalyzedData:
    status = ["三空叩き込み",         #0
              "三手大陰線",           #1
              "最後の抱き陰線",       #2
              "明けの明星",           #3
              "捨て子底",             #4
              "大陰線のはらみ寄せ",   #5
              "たくり線",             #6
              "勢力線",               #7
              "陰の陰はらみ",         #8
              "放れ五手黒一本底",     #9
              "やぐら底",             #10
              "小幅上放れ黒線",       #11
              "放れ七手の変化底",     #12
              "連続下げ放れ三つ星",   #13
              "逆襲線",               #14
              "抱き陽線",             #15
              "寄り切り陽線",         #16
              "赤三兵",               #17
              "下位の陽線五本",       #18
              "押え込み線",           #19
              "上げの差し込み線",     #20
              "上げ三法",             #21
              "カブセの上抜け",       #22
              "上伸途上の連続タスキ", #23
              "上放れタスキ",         #24
              "上伸途上のクロス",     #25
              "上げの三つ星",         #26
              "並び赤",               #27
              "上放れ陰線二本連続",   #28
              "上位の連続大陽線",     #29
              "波高い線",             #30
              "三空踏み上げ",         #31
              "新値八手利食い線",     #32
              "三手放れ寄せ線",       #33
              "行き詰まり線",         #34
              "三羽ガラス",           #35
              "首吊り線",             #36
              "上位の上放れ陰線",     #37
              "宵の明星",             #38
              "陽の陽はらみ",         #39
              "最後の抱き陽線",       #40
              "抱き陽線",             #41
              "つたい線の打ち返し",   #42
              "放れ五手赤一本",       #43
              "放れ七手大黒",         #44
              "差し込み線",           #45
              "下放れ三手",           #46
              "下げ三法",             #47
              "三手打ち",             #48
              "下落途上の連続タスキ", #49
              "化け線",               #50
              "下げ足のクロス",       #51
              "下放れ黒二本",         #52
              "下げの三つ星",         #53
              "上位の陰線五本",       #54
              "寄り切り陰線",         #55
              "予約01",               #56
              "予約02",               #57
              "予約03",               #58
              "予約04",               #59
              "予約05",               #60
              "予約06",               #61
              "予約07",               #61
              "予約08",               #63
              "予約09",               #64
              "予約00",               #65
              "予約01",               #66
              "予約02",               #67
              "予約03",               #68
              "予約04"               #69
              ]
    
    state = -1

    def __init__(self) -> None:
        self.state = -1
        pass    
    
    def setStatus(self,state):
        self.state = state

    def getAnzlyzedData(self):
        return self.state
    
    def getAnzlyzedDataString(self):
        if self.state == -1:
            return ""
        return self.status[self.state]
    
class Data:
    date             = ""
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

    maxValue = 0.0
    minValue = 0.0

    positive = False
    negative = False
    bigPositive = False
    bigNegative = False
    smallPositive = False
    smallNegative = False
    tinyPositive = False
    tinyNegative = False

    cross = False

    candleState = None

    analysis1Row = None
    analysis2Rows = None
    analysis3Rows = None
    analysis4Rows = None
    analysis5Rows = None
    analysis6Rows = None
    analysis7Rows = None
    analysis8Rows = None
    highBeard = False
    higherBeard = False
    lowBeard = False
    lowerBeard = False

    desc = False
    asce = False
    flat     = False

    includedFromPrev = False
    includePrev = False
    
    hasWindowRegion = False

    isNoneValue = False

    windowFactor = 0.1
    beardFactor = 0.1
    

    def __init__(self,data,windoFactor,beardFactor) -> None:
        self.candleState   = CandleState()
        self.analysis1Row  = AnalyzedData()
        self.analysis2Rows = AnalyzedData()
        self.analysis3Rows = AnalyzedData()
        self.analysis4Rows = AnalyzedData()
        self.analysis5Rows = AnalyzedData()
        self.analysis6Rows = AnalyzedData()
        self.analysis7Rows = AnalyzedData()
        self.analysis8Rows = AnalyzedData()
        self.desc = False
        self.asce = False
        self.flat = False
        self.includeedFromPrev = False
        self.includePrev = False
        self.hasWindowRegion = False
        self.windowFactor = windoFactor
        self.beardFactor = beardFactor

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

        self.maxValue =0.0
        self.minValue =0.0

        self.negative = False
        self.positive = False
        self.bigNegative = False
        self.bigPositive = False
        self.smallNegative = False
        self.smallPositive = False
        self.tinyNegative = False
        self.tinyPositive = False

        self.highBeard = False
        self.lowBeard = False

        self.higherBeard = False
        self.lowerBeard = False

        if self.open > self.close:
            self.maxValue = self.open
            self.minValue = self.close
            self.negative = True
            self.candleState.setState(10)
            if self.open > self.close*1.10:
                self.bigNegative = True
                if self.high > self.open and self.low < self.close:
                    self.candleState.setState(11)
                if self.high == self.open and self.low == self.close:
                    self.candleState.setState(12)
                if self.high == self.open and self.low < self.close:
                    self.candleState.setState(13)
                if self.high > self.open and self.low == self.close:
                    self.candleState.setState(14)
            if self.close* 1.03 < self.open <= self.close*1.10:
                self.smallNegative = True
                if self.high > self.open and self.low < self.close:
                    self.candleState.setState(15)
                if self.high > self.open and self.low < self.close and (self.high - self.open) < (self.close - self.low):
                    self.candleState.setState(16)
                if self.high > self.open * (1 + self.beardFactor) and self.low  * (1 + self.beardFactor) < self.close:
                    self.candleState.setState(17)
                if self.high > self.open and self.low < self.close and (self.high - self.open) > (self.close - self.low):
                    self.candleState.setState(18)
                if self.high == self.open and self.low * (1 + self.beardFactor) < self.close:
                    self.candleState.setState(19)
            if self.open <= self.close *1.03:
                self.tinyNegative = True
            if self.high > self.open:
                self.highBeard = True
                if self.high >= self.open*(1+beardFactor):
                    self.higherBeard = True
            if self.low < self.close:
                self.lowBeard = True
                if self.low*(1+beardFactor) < self.close:
                    self.lowerBeard = True
        elif self.close > self.open:
            self.maxValue = self.close
            self.minValue = self.open
            self.positive = True
            self.candleState.setState(0)
            if self.close > self.open*1.10:
                self.bigPositive = True
                if self.high > self.close and self.low < self.open:
                    self.candleState.setState(1)
                if self.high == self.close and self.low == self.open:
                    self.candleState.setState(2)
                if self.high == self.close and self.low < self.open:
                    self.candleState.setState(3)
                if self.high > self.close and self.low == self.open:
                    self.candleState.setState(4)                    
            if self.open* 1.03 < self.close <= self.open*1.10:
                self.smallPositive = True
                if self.high > self.close and self.low < self.open:
                    self.candleState.setState(5)
                if self.high > self.close and self.low < self.open and (self.high - self.close) < (self.open - self.low):
                    self.candleState.setState(6)
                if self.high > self.close * (1 + self.beardFactor) and self.low  * (1 + self.beardFactor) < self.open:
                    self.candleState.setState(7)
                if self.high > self.close and self.low < self.open and (self.high - self.close) > (self.open - self.low):
                    self.candleState.setState(8)
                if self.high == self.close and self.low * (1 + self.beardFactor) < self.open:
                    self.candleState.setState(9)
            if self.close <= self.open*1.03:
                self.tinyPositive = True
            if self.high > self.close:
                self.highBeard = True
                if self.high >= self.close*(1+beardFactor):
                    self.higherBeard = True
            if self.low < self.open:
                self.lowBeard = True
                if self.low*(1+beardFactor) < self.open:
                    self.lowerBeard = True
        else:
            self.maxValue = self.open
            self.minValue = self.open
            self.cross = True
            if self.high > self.open and self.open > self.low:
                self.candleState.setState(20)
            if self.high == self.open and self.open > self.low:
                self.candleState.setState(21)
            if self.high > self.open and self.open > self.low and ((self.high - self.open)*(1 + self.beardFactor) < (self.open - self.low)):
                self.candleState.setState(22)
            if (self.high - self.open) >  (self.open * self.beardFactor) and (self.open - self.low) > (self.open * self.beardFactor):
                self.candleState.setState(23)
            if self.high > self.open and self.open == self.low:
                self.candleState.setState(24)
            if self.high == self.open and self.open == self.low:
                self.candleState.setState(25)
            if self.high > self.open:
                self.highBeard = True
                if self.high >= self.open*(1+beardFactor):
                    self.higherBeard = True
            if self.low < self.open:
                self.lowBeard = True
                if self.low*(1+beardFactor) < self.open:
                    self.lowerBeard = True

    def write(self,worksheet,count):
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
        worksheet[f'P{count}']  = self.getCandleState().getStateString()
        worksheet[f'Q{count}']  = self.getFactor()
        worksheet[f'R{count}']  = self.minValue
        worksheet[f'S{count}']  = self.maxValue
        worksheet[f'AA{count}']  = self.get1RowStatus().getAnzlyzedDataString()
        worksheet[f'AB{count}']  = self.get2RowsStatus().getAnzlyzedDataString()
        worksheet[f'AC{count}']  = self.get3RowsStatus().getAnzlyzedDataString()
        worksheet[f'AD{count}']  = self.get4RowsStatus().getAnzlyzedDataString()
        worksheet[f'AA{count}']  = self.get5RowsStatus().getAnzlyzedDataString()
        worksheet[f'AB{count}']  = self.get6RowsStatus().getAnzlyzedDataString()
        worksheet[f'AC{count}']  = self.get7RowsStatus().getAnzlyzedDataString()
        worksheet[f'AD{count}']  = self.get8RowsStatus().getAnzlyzedDataString()
        worksheet[f'AE{count}']  = ""
        worksheet[f'AF{count}']  = ""
        worksheet[f'AG{count}']  = ""
        worksheet[f'AH{count}'] = ""
        worksheet[f'AI{count}'] = ""
        worksheet[f'AJ{count}'] = ""
        worksheet[f'AK{count}'] = ""

    def setFactor(self,prev):
        if prev.max() == self.max() and prev.min() == prev.min():
            self.flat = True
            return 
        if prev.max() > self.max() and prev.min() < self.min():
            self.includedPrev = True
            return 
        if prev.max() < self.max() and prev.min() > self.min():
            self.includePrev = True
            return
        if prev.max() < self.max():
            if prev.max()*(1+self.windowFactor) <= self.min():
                self.hasWindowRegion = True    
            self.asce = True
            return
        if prev.min() > self.min():
            if prev.min() >= self.max()*(1.0+self.windowFactor):
                self.hasWindowRegion = True    
            self.desc = True
            return

    def isFlat(self):
        return self.flat

    def isIncludedFromPrev(self):
        return self.includedFromPrev

    def isIncludePrev(self):
        return self.includedPrev

    def hasWindow(self):
        return self.hasWindowRegion

    def isDesc(self):
        return self.desc

    def isAsce(self):
        return self.asce
    
    def printFactors(self):
        print (f'cross={self.cross},includedFromPrev={self.includedFromPrev},includePrev={self.includePrev},hasWindow={self.hasWindowRegion},Desc={self.desc},Asce={self.asce}')

    def getOpen(self):
        return self.open

    def getHigh(self):
        return self.high

    def getLow(self):
        return self.low

    def getClose(self):
        return self.close

    def min(self):
        return self.minValue
    
    def max(self):
        return self.maxValue
    
    def isNone(self):
        return self.isNoneValue
    
    def getAvg(self):
        return (self.open + self.high + self.low + self.close) / 4

    def getFactor(self):
        return (self.maxValue -self.minValue)/self.getAvg()

    def getRatio(self):
        return self.getFactor()

    def getAbsFactor(self):
        return abs(self.getFactor())

    def getAbsRatio(self):  
        return self.getAbsFactor()
        
    def isPositive(self):
        return self.positive

    def isNegative(self):
        return self.negative
        
    def isBigPositive(self):
        return self.bigPositive

    def isBigNegative(self):
        return self.bigNegative

    def isSmallPositive(self):
        return self.smallPositive

    def isSmallNegative(self):
        return self.smallNegative

    def isTinyPositive(self):
        return self.tinyPositive

    def isTinyNegative(self):
        return self.tinyNegative

    def isCross(self):
        return self.cross
    
    def isBig(self):
        return self.isBigNegative() or self.isBigPositive()

    def isSmall(self):
        return self.isBigNegative() or self.isBigPositive()

    def isTiny(self):
        return self.isTinyNegative() or self.isTinyPositive()

    def getCandleState(self):
        return self.candleState

    def getCandleStateString(self):
        return self.candleState.getState()
    
    def set1RowStatus(self,status):
        self.analysis1Row.setStatus(status)

    def get1RowStatus(self):
        return self.analysis1Row

    def set2RowsStatus(self,status):
        self.analysis2Rows.setStatus(status)

    def get2RowsStatus(self):
        return self.analysis2Rows

    def set3RowsStatus(self,status):
        self.analysis3Rows.setStatus(status)

    def get3RowsStatus(self):
        return self.analysis3Rows

    def set4RowsStatus(self,status):
        self.analysis4Rows.setStatus(status)

    def get4RowsStatus(self):
        return self.analysis4Rows

    def set5RowsStatus(self,status):
        self.analysis5Rows.setStatus(status)

    def get5RowsStatus(self):
        return self.analysis5Rows

    def set6RowsStatus(self,status):
        self.analysis6Rows.setStatus(status)

    def get6RowsStatus(self):
        return self.analysis6Rows
    
    def set7RowsStatus(self,status):
        self.analysis7Rows.setStatus(status)

    def get7RowsStatus(self):
        return self.analysis7Rows
    
    def set8RowsStatus(self,status):
        self.analysis8Rows.setStatus(status)

    def get8RowsStatus(self):
        return self.analysis8Rows
