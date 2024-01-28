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
                   'カラカサ(たぐり線)',
                   'トンカチ(たぐり線)',
                   'カラカサ(たぐり線)',
                   'トンカチ(たぐり線)',
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

class CandleStick:

    type = None

    def __init__(self,open,high,low,close) -> None:

        openCloseRatio = CandleStick.calcOpenCloseRatio(open,close)
        lowBeardRatio = CandleStick.calcLowBeardRatio(open,high,low,close)
        highBeardRatio = CandleStick.calcHighBeardRatio(open,high,low,close)
        
        #threeType = ['-','陰線','陽線','寄引同時線']
        #nineType = ['-','大陰線','大陽線','小陰線','小陽線','上ヒゲ陰線','上ヒゲ陽線','下ヒゲ陰線','下ヒゲ陽線','寄引同時線']
        #seventeenType = ['-','陰の丸坊主','陽の丸坊主','陰の大引坊主','陰の寄付坊主','陽の寄付坊主','陽の大引坊主','コマ(陰の極線)','コマ(陽の極線)','トンボ','トンボ','トウバ(石塔)','足長同時(寄せ場)','カラカサ(たぐり線)','トンカチ(たぐり線)','カラカサ(たぐり線)','トンカチ(たぐり線)','四値同時(一本同時)']

        if open == close: #寄引同時線
            if lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio == 0.0: #トンボ
                self.candleStickType = CandleStickType(3,9,9)    
            elif highBeardRatio > CommonPackage.highLowBigSmallThreshold and lowBeardRatio == 0.0: #トウバ(石塔)
                self.candleStickType = CandleStickType(3,9,11)
            elif lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio < CommonPackage.highLowBigSmallThreshold: #トンボ
                self.candleStickType = CandleStickType(3,9,10) 
            elif lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio > CommonPackage.highLowBigSmallThreshold: #足長同時(寄せ場)
                self.candleStickType = CandleStickType(3,9,12) 
            else:
                self.candleStickType = CandleStickType(3,9,0) #寄引同時線

        #threeType = ['-','陰線','陽線','寄引同時線']
        #nineType = ['-','大陰線','大陽線','小陰線','小陽線','上ヒゲ陰線','上ヒゲ陽線','下ヒゲ陰線','下ヒゲ陽線','寄引同時線']
        #seventeenType = ['-','陰の丸坊主','陽の丸坊主','陰の大引坊主','陰の寄付坊主','陽の寄付坊主','陽の大引坊主','コマ(陰の極線)','コマ(陽の極線)','トンボ','トンボ','トウバ(石塔)','足長同時(寄せ場)','カラカサ(たぐり線)','トンカチ(たぐり線)','カラカサ(たぐり線)','トンカチ(たぐり線)','四値同時(一本同時)']

        if open > close: #陰線
            if  openCloseRatio > CommonPackage.openCloseBigSmallThreshold: #大陰線
                if highBeardRatio == 0.0 and lowBeardRatio == 0.0: #陰の丸坊主
                    self.candleStickType = CandleStickType(1,1,1)
                else: #大陰線
                    if highBeardRatio > CommonPackage.highLowBigSmallThreshold and lowBeardRatio == 0.0: #陰の大引坊主
                        self.candleStickType = CandleStickType(1,1,3)
                    elif lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio == 0.0: #陰の寄付坊主
                        self.candleStickType = CandleStickType(1,1,4)
                    else:
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

        #threeType = ['-','陰線','陽線','寄引同時線']
        #nineType = ['-','大陰線','大陽線','小陰線','小陽線','上ヒゲ陰線','上ヒゲ陽線','下ヒゲ陰線','下ヒゲ陽線','寄引同時線']
        #seventeenType = ['-','陰の丸坊主','陽の丸坊主','陰の大引坊主','陰の寄付坊主','陽の寄付坊主','陽の大引坊主','コマ(陰の極線)','コマ(陽の極線)','トンボ','トンボ','トウバ(石塔)','足長同時(寄せ場)','カラカサ(たぐり線)','トンカチ(たぐり線)','カラカサ(たぐり線)','トンカチ(たぐり線)','四値同時(一本同時)']

        if open < close: #陽線
            if openCloseRatio > CommonPackage.openCloseBigSmallThreshold: #大陽線
                if highBeardRatio == 0.0 and lowBeardRatio == 0.0:  #陽の丸坊主
                    self.candleStickType = CandleStickType(2,2,2)
                else: #大陽線
                    if highBeardRatio > CommonPackage.highLowBigSmallThreshold and lowBeardRatio == 0.0: #陽の寄付坊主
                        self.candleStickType = CandleStickType(2,2,5)
                    elif lowBeardRatio > CommonPackage.highLowBigSmallThreshold and highBeardRatio == 0.0: #陽の大引坊主
                        self.candleStickType = CandleStickType(2,2,6)
                    else:
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
        #fifteenType = ['-','陰の丸坊主','陽の丸坊主','陰の大引坊主','陰の寄付坊主','陽の寄付坊主','陽の大引坊主','コマ(陰の極線)','コマ(陽の極線)','トンボ','トンボ','トウバ(石塔)','足長同時(寄せ場)','カラカサ(たぐり線)','カラカサ(たぐり線)','四値同時(一本同時)']


    def getThreeTypeString(self):
        return self.candleStickType.getThreeTypeString()
    
    def getNineTypeString(self):
        return self.candleStickType.getNineTypeString()
    
    def getSeventeenTypeString(self):
        return self.candleStickType.getSeventeenTypeString()
    
    def calcOpenCloseRatio(open,close):
        return abs(open-close) / min(open,close)
    
    def calcLowBeardRatio(open,high,low,close):
        return (min(open,close) - low) / min(open,close)
    
    def calcHighBeardRatio(open,high,low,close):
        return (high - max(open,close)) / max(open,close)