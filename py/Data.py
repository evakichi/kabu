import CommonPackage

class Data:
    open  = 0.0
    high  = 0.0
    low   = 0.0
    close = 0.0
    isNone = False

            worksheet[f"A{quoteCount}"] = daily_quote['Date']
            worksheet[f"B{quoteCount}"] = daily_quote['Open']
            worksheet[f"C{quoteCount}"] = daily_quote['High']
            worksheet[f"D{quoteCount}"] = daily_quote['Low']
            worksheet[f"E{quoteCount}"] = daily_quote['Close']
            worksheet[f"F{quoteCount}"] = daily_quote['UpperLimit']
            worksheet[f"G{quoteCount}"] = daily_quote['LowerLimit']
            worksheet[f"H{quoteCount}"] = daily_quote['Volume']
            worksheet[f"I{quoteCount}"] = daily_quote['TurnoverValue']
            worksheet[f"J{quoteCount}"] = daily_quote['AdjustmentFactor']
            worksheet[f"K{quoteCount}"] = daily_quote['AdjustmentOpen']
            worksheet[f"L{quoteCount}"] = daily_quote['AdjustmentHigh']
            worksheet[f"M{quoteCount}"] = daily_quote['AdjustmentLow']
            worksheet[f"N{quoteCount}"] = daily_quote['AdjustmentClose']
            worksheet[f"O{quoteCount}"] = daily_quote['AdjustmentVolume']


    def __init__(self,open,high,low,close,upperLimit,lowerLimit,volume,) -> None:
        if open == None or high == None or low == None or close == None:
            self.isNone = True
            return
        self.open  = float(open)
        self.high  = float(high)
        self.low   = float(low)
        self.close = float(close)
        pass

    def min(self):
        if not self.isNone and self.open < self.close:
            return self.open
        return self.close

    def max(self):
        if not self.isNone and self.open > self.close:
            return self.open
        return self.close

    def isNone(self):
        return self.isNone
    
    def getAvg(self):
        return (self.open + self.high + self.low + self.close) / 4

    def getRatio(self):
        return (self.close - self.open) / self.getAvg()

    def getAbsRatio(self):
        return abs(self.getRatio())
    
    def isPositive(self):
        if not self.isNone and self.open < self.close:
            return True
        return False

    def isNegative(self):
        if not self.isNone and self.open > self.close:
            return True
        return False

    def isCross(self):
        if not self.isNone and self.open == self.close:
            return True
        return False

    def isSmallPositive(self):
        if self.isPositive():
            if self.getAbsRatio() < 0.1:
                return True
        return False

    def isBigPositive(self):
        if self.isPositive():
            if self.getAbsRatio() >= 0.1:
                return True
        return False

    def isSmallNegative(self):
        if self.isNegative():
            if self.getAbsRatio() < 0.1:
                return True
        return False

    def isBigNegative(self):
        if self.isNegative():
            if self.getAbsRatio() >= 0.1:
                return True
        return False
    
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