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

        openCloseRatio = CandleStick.calcOpenCloseRatio(open,close)
        lowBeardRatio = CandleStick.calcLowBeardRatio(open,high,low,close)
        highBeardRatio = CandleStick.calcLowBeardRatio(open,high,low,close)
        
        if open == close: #寄引同時線
            self.candleStickType = CandleStickType(3,9,0)
        if open > close: #陰線
            if  openCloseRatio > CommonPackage.openCloseBigSmallThreshold: #大陰線
                self.candleStickType = CandleStickType(1,1,0) 
            else: #小陰線
                if highBeardRatio > lowBeardRatio: 
                    if highBeardRatio > CommonPackage.highLowBigSmallThreshold: #上ヒゲ陰線
                        self.candleStickType = CandleStickType(1,5,0)
                    else: #小陰線
                        self.candleStickType = CandleStickType(1,3,0)
                else:
                    if highBeardRatio > CommonPackage.highLowBigSmallThreshold: #下ヒゲ陰線
                        self.candleStickType = CandleStickType(1,7,0)
                    else: #小陰線
                        self.candleStickType = CandleStickType(1,3,0)
        if open < close: #陽線
            if openCloseRatio > CommonPackage.openCloseBigSmallThreshold: #大陽線
                self.candleStickType = CandleStickType(2,2,0)
            else: #小陽線
                if highBeardRatio > lowBeardRatio:
                    if highBeardRatio > CommonPackage.highLowBigSmallThreshold: #上ヒゲ陽線
                        self.candleStickType = CandleStickType(2,6,0)
                    else: #小陰線
                        self.candleStickType = CandleStickType(2,4,0)
                else:
                    if highBeardRatio > CommonPackage.highLowBigSmallThreshold: #下ヒゲ陽線
                        self.candleStickType = CandleStickType(2,8,0)
                    else: #小陰線
                        self.candleStickType = CandleStickType(2,4,0)

        #threeType = ['-','陰線','陽線','寄引同時線']
        #nineType = ['-','大陰線','大陽線','小陰線','小陽線','上ヒゲ陰線','上ヒゲ陽線','下ヒゲ陰線','下ヒゲ陽線','寄引同時線']
        #fifteenType = ['-','大陰線','大陽線','小陰線','小陽線','上ヒゲ陰線','上ヒゲ陽線','下ヒゲ陰線','下ヒゲ陽線','寄引同時線']


    def getThreeTypeString(self):
        return self.candleStickType.getThreeTypeString()
    
    def getNineTypeString(self):
        return self.candleStickType.getNineTypeString()
    
    def getFifteenTypeString(self):
        return self.candleStickType.getFifteenTypeString()
    
    def calcOpenCloseRatio(open,close):
        return abs(open-close) / min(open,close)
    
    def calcLowBeardRatio(open,high,low,close):
        return (min(open,close) - low) / min(open,close)
    
    def calcHighBeardRatio(open,high,low,close):
        return (high - max(open,close)) / max(open,close)