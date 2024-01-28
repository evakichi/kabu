import CommonPackage
import Quotes

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
    seventeenType = ['-',
                   '陰の丸坊主',
                   '陽の丸坊主',
                   '陰の大引坊主',
                   '陰の寄付坊主',
                   '陽の寄付坊主',
                   '陽の大引坊主',
                   'コマ(陰の極線)',
                   'コマ(陽の極線)',
                   'トンボ',
                   'トンボ',
                   'トウバ(石塔)',
                   '足長同時(寄せ場)',
                   '陰のカラカサ(たぐり線)',
                   '陰のトンカチ(たぐり線)',
                   '陽のカラカサ(たぐり線)',
                   '陽のトンカチ(たぐり線)',
                   '四値同時(一本同時)'
                   ]

    def __init__(self,threeTypeCode,nineTypeCode,seventeenTypeCode) -> None:
        self.threeTypeCode = threeTypeCode
        self.nineTypeCode = nineTypeCode
        self.seventeenTypeCode = seventeenTypeCode
        pass

    def getThreeTypeString(self):
        return self.threeType[self.threeTypeCode]

    def getNineTypeString(self):
        return self.nineType[self.nineTypeCode]

    def getSeventeenTypeString(self):
        return self.seventeenType[self.seventeenTypeCode]

    def getThreeTypeCode(self):
        return self.threeTypeCode

    def getNineTypeCode(self):
        return self.nineTypeCode

    def getSeventeenTypeCode(self):
        return self.seventeenTypeCode

class CandleStick:

    type = None

    def __init__(self,quotes) -> None:

        self.candleStickType = CandleStick.calcCandleStickType(quotes)

    def calcCandleStickType(quotes):

        if quotes == None:
            return None

        openCloseRatio = CandleStick.calcOpenCloseRatio(quotes.open,quotes.close)
        lowBeardRatio = CandleStick.calcLowBeardRatio(quotes.open,quotes.high,quotes.low,quotes.close)
        highBeardRatio = CandleStick.calcHighBeardRatio(quotes.open,quotes.high,quotes.low,quotes.close)
        
        if quotes.open == quotes.close: 
            if lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio == 0.0:
                return CandleStickType(3,9,9)
            if lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio < CommonPackage.highLowBigSmallThreshold:
                return CandleStickType(3,9,10)
            if lowBeardRatio == 0.0 and highBeardRatio > CommonPackage.highLowBigSmallThreshold:
                return CandleStickType(3,9,11)
            if lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio > CommonPackage.highLowBigSmallThreshold:
                return CandleStickType(3,9,12)
            if lowBeardRatio == 0.0 and highBeardRatio == 0.0:
                return CandleStickType(3,9,17)
            return CandleStickType(3,9,0)
        
        if quotes.open > quotes.close:
            if openCloseRatio > CommonPackage.openCloseBigSmallThreshold:
                if quotes.open == quotes.high and quotes.close == quotes.low:
                    return CandleStickType(1,1,1)
                if highBeardRatio > CommonPackage.highLowBigSmallThreshold and quotes.close == quotes.low:
                    return CandleStickType(1,1,3)
                if lowBeardRatio > CommonPackage.highLowBigSmallThreshold and quotes.open == quotes.high:
                    return CandleStickType(1,1,4)
            else:
                if highBeardRatio != 0.0 and highBeardRatio < CommonPackage.highLowBigSmallThreshold and lowBeardRatio != 0.0 and lowBeardRatio < CommonPackage.highLowBigSmallThreshold:
                    return CandleStickType(1,3,7)
                if highBeardRatio == 0.0 and lowBeardRatio > CommonPackage.highLowBigSmallThreshold:
                    return CandleStickType(1,3,13)
                if lowBeardRatio == 0.0 and highBeardRatio > CommonPackage.highLowBigSmallThreshold:
                    return CandleStickType(1,3,14)
            return CandleStickType(1,1,0)

        if quotes.open < quotes.close:
            if openCloseRatio > CommonPackage.openCloseBigSmallThreshold:
                if quotes.open == quotes.high and quotes.close == quotes.low:
                    return CandleStickType(2,2,2)
                if highBeardRatio > CommonPackage.highLowBigSmallThreshold and quotes.open == quotes.low:
                    return CandleStickType(2,2,5)
                if lowBeardRatio > CommonPackage.highLowBigSmallThreshold and quotes.close == quotes.high:
                    return CandleStickType(2,2,6)
            else:
                if highBeardRatio != 0.0 and highBeardRatio < CommonPackage.highLowBigSmallThreshold and lowBeardRatio != 0.0 and lowBeardRatio < CommonPackage.highLowBigSmallThreshold:
                    return CandleStickType(2,4,8)
                if highBeardRatio == 0.0 and lowBeardRatio > CommonPackage.highLowBigSmallThreshold:
                    return CandleStickType(2,4,15)
                if lowBeardRatio == 0.0 and highBeardRatio > CommonPackage.highLowBigSmallThreshold:
                    return CandleStickType(2,4,16)
            return CandleStickType(2,4,0)
        return (0,0,0)

    def getThreeTypeString(self):
        return self.candleStickType.getThreeTypeString()
    
    def getNineTypeString(self):
        return self.candleStickType.getNineTypeString()
    
    def getSeventeenTypeString(self):
        return self.candleStickType.getSeventeenTypeString()
    
    def getThreeTypeCode(self):
        return self.candleStickType.getThreeTypeCode()
    
    def getNineTypeCode(self):
        return self.candleStickType.getNineTypeCode()
    
    def getSeventeenTypeCode(self):
        return self.candleStickType.getSeventeenTypeCode()
    
    def calcOpenCloseRatio(open,close):
        return abs(open-close) / min(open,close)
    
    def calcLowBeardRatio(open,high,low,close):
        return (min(open,close) - low) / min(open,close)
    
    def calcHighBeardRatio(open,high,low,close):
        return (high - max(open,close)) / max(open,close)