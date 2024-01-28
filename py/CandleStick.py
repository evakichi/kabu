import CommonPackage

class CandleStickType:

    threeType = ['-',
                 '陰線',
                 '陽線',
                 '寄引同時線'
                 ]

    nineType = ['-',
                '大陰線',
                '大陽線',
                '小陰線',
                '小陽線',
                '上ヒゲ陰線',
                '上ヒゲ陽線',
                '下ヒゲ陰線',
                '下ヒゲ陽線',
                '寄引同時線'
                ]

    fifteenType = ['-',
                   '大陰線',
                   '大陽線',
                   '小陰線',
                   '小陽線',
                   '上ヒゲ陰線',
                   '上ヒゲ陽線',
                   '下ヒゲ陰線',
                   '下ヒゲ陽線',
                   '寄引同時線'
                   ]

    def __init__(self,threeTypeCode,nineTypeCode,fifteenTypeCode) -> None:
        self.threeTypeCode = threeTypeCode
        self.nineTypeCode = nineTypeCode
        self.fifteenTypeCode = fifteenTypeCode
        pass

    def getThreeTypeString(self):
        return self.threeType[self.threeTypeCode]

    def getNineTypeString(self):
        return self.nineType[self.nineTypeCode]

    def getFifteenTypeString(self):
        return self.fifteenType[self.fifteenTypeCode]

class CandleStick:

    type = None

    def __init__(self,open,high,low,close) -> None:

        if open == close:
            self.candleStickType = CandleStickType(3,9,0)
        if open > close:
            if CandleStick.calcOpenCloseRatio(open,close) > CommonPackage.openCloseBigSmallThreshold:
                self.candleStickType = CandleStickType(1,1,0)
            else:
                self.candleStickType = CandleStickType(1,3,0)
        if open < close:
            if CandleStick.calcOpenCloseRatio(open,close) > CommonPackage.openCloseBigSmallThreshold:
                self.candleStickType = CandleStickType(2,2,0)
            else:
                self.candleStickType = CandleStickType(2,4,0)


    def getThreeTypeString(self):
        return self.candleStickType.getThreeTypeString()
    
    def getNineTypeString(self):
        return self.candleStickType.getNineTypeString()
    
    def getFifteenTypeString(self):
        return self.candleStickType.getFifteenTypeString()
    
    def calcOpenCloseRatio(open,close):
        return abs(open-close)/min(open,close)