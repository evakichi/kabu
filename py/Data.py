import sys

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
              "寄り切り陰線"          #55
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
    analysis5Days = None
    analysis6Days = None
    analysis7Days = None
    analysis8Days = None

    isNoneValue = False

    def __init__(self,data) -> None:
        self.analysis5Days = AnalyzedData()
        self.analysis6Days = AnalyzedData()
        self.analysis7Days = AnalyzedData()
        self.analysis8Days = AnalyzedData()
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
        worksheet[f'P{count}']  = self.getCandleState()
        worksheet[f'Q{count}']  = self.getRatio()
        worksheet[f'R{count}']  = self.min()
        worksheet[f'S{count}']  = self.max()
        worksheet[f'AA{count}']  = self.get5DaysStatus().getAnzlyzedDataString()
        worksheet[f'AB{count}']  = self.get6DaysStatus().getAnzlyzedDataString()
        worksheet[f'AC{count}']  = self.get7DaysStatus().getAnzlyzedDataString()
        worksheet[f'AD{count}']  = self.get8DaysStatus().getAnzlyzedDataString()
        worksheet[f'AE{count}']  = ""
        worksheet[f'AF{count}']  = ""
        worksheet[f'AG{count}']  = ""
        worksheet[f'AH{count}'] = ""
        worksheet[f'AI{count}'] = ""
        worksheet[f'AJ{count}'] = ""
        worksheet[f'AK{count}'] = ""

    def getOpen(self):
        return self.open

    def getHigh(self):
        return self.high

    def getLow(self):
        return self.low

    def getClose(self):
        return self.close

    def min(self):
        if not self.isNoneValue:
            if self.open < self.close:
                return self.open
            return self.close
        return -1*(sys.maxsize-1)

    def max(self):
        if not self.isNoneValue:
            if self.open > self.close:
                return self.open
            return self.close
        return sys.maxsize-1

    def isNone(self):
        return self.isNoneValue
    
    def getAvg(self):
        if self.isNoneValue:
            return 0.0
        return (self.open + self.high + self.low + self.close) / 4

    def getRatio(self):
        if self.isNoneValue:
            return 0.0
        return (self.close - self.open) / self.getAvg()

    def getAbsRatio(self):
        if self.isNoneValue:
            return 0.0
        return abs(self.getRatio())
    
    def isPositive(self):
        if not self.isNoneValue and self.open < self.close:
            return True
        return False

    def isNegative(self):
        if not self.isNoneValue and self.open > self.close:
            return True
        return False

    def isCross(self):
        if not self.isNoneValue and self.open == self.close:
            return True
        return False

    def isSmallPositive(self):
        if self.isPositive():
            if self.getAbsRatio() < 0.03:
                return True
        return False

    def isBigPositive(self):
        if self.isPositive():
            if self.getAbsRatio() >= 0.1:
                return True
        return False

    def isSmallNegative(self):
        if self.isNegative():
            if self.getAbsRatio() < 0.03:
                return True
        return False

    def isBigNegative(self):
        if self.isNegative():
            if self.getAbsRatio() >= 0.1:
                return True
        return False

    def isBig(self):
        return self.isBigNegative() or self.isBigPositive()

    def isSmall(self):
        return self.isBigNegative() or self.isBigPositive()

    def getCandleState(self):
        if self.isBigNegative():
            return "大陰線"
        if self.isSmallNegative():
            return "小陰線"
        if self.isBigPositive():
            return "大陽線"
        if self.isSmallPositive():
            return "小陽線"
        return "十字線"
    
    def set5DaysStatus(self,status):
        self.analysis5Days.setStatus(status)

    def get5DaysStatus(self):
        return self.analysis5Days

    def set6DaysStatus(self,status):
        self.analysis6Days.setStatus(status)

    def get6DaysStatus(self):
        return self.analysis6Days
    
    def set7DaysStatus(self,status):
        self.analysis7Days.setStatus(status)

    def get7DaysStatus(self):
        return self.analysis7Days
    
    def set8DaysStatus(self,status):
        self.analysis8Days.setStatus(status)

    def get8DaysStatus(self):
        return self.analysis8Days
