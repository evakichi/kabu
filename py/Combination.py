import CommonPackage

class CombinationType:
     
     combinationType=['-',
                      'かぶせ線',#1
                      'あて首線',#2
                      '入り首線',#3
                      '差込み線',#4
                      '切込み線',#5
                      'たすき線',#6
                      '包み線',#7
                      'はらみ線',#8
                      '星',#9
                      '出合い線',#10
                      '行き違い線',#11
                      '並び赤',#12
                      '並び黒',#13
                      '毛抜き線',#14
                      '連続線',#15
                      '空(くう)'#16
                      ]
     def __init__(self,code) -> None:
          self.combinationCode = code
          pass
     
     def getString(self):
          return self.combinationType[self.combinationCode]
     
class Combination:
    
    combinationType  = None
    isNone = False

    def __init__(self,prev,current) -> None:
        if prev == None or current == None:
            isNone = True
            return None
        self.combinationType = Combination.calcCombinationType(prev,current)       
    
    def calcCombinationType(prev,current):
        if prev.quotes == None:
            return None

        if prev.candleStick.getThreeTypeCode() == 2 and current.candleStick.getThreeTypeCode() == 1 and prev.quotes.high == current.quotes.open:
            return CombinationType(14) #毛抜き線
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getThreeTypeCode() == 2 and prev.quotes.low == current.quotes.open:
            return CombinationType(14) #毛抜き線
        if prev.candleStick.getThreeTypeCode() == 2 and current.candleStick.getThreeTypeCode() == 1 and prev.quotes.open < current.quotes.close and prev.quotes.close > current.quotes.close and prev.quotes.close < current.quotes.open:
            return CombinationType(1) #かぶせ線
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getThreeTypeCode() == 2 and prev.quotes.close > current.quotes.close:
            return CombinationType(2) #あて首線
        if prev.candleStick.getNineTypeCode() == 1 and current.candleStick.getNineTypeCode() == 2 and prev.quotes.close < current.quotes.close and prev.quotes.open > current.quotes.close:
            return CombinationType(5) #切込み線
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getNineTypeCode() == 2 and prev.quotes.close < current.quotes.close and prev.quotes.open > current.quotes.close:
            return CombinationType(4) #差込み線
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getThreeTypeCode() == 2 and prev.quotes.close < current.quotes.close and prev.quotes.open > current.quotes.close:
            return CombinationType(3) #入り首線
        if prev.candleStick.getThreeTypeCode() == 2 and current.candleStick.getThreeTypeCode() == 1 and prev.quotes.open < current.quotes.open and prev.quotes.close > current.quotes.open:
            return CombinationType(6) #たすき線
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getThreeTypeCode() == 2 and prev.quotes.open > current.quotes.open and prev.quotes.close < current.quotes.open:
            return CombinationType(6) #たすき線
        if prev.candleStick.getThreeTypeCode() == 2 and current.candleStick.getThreeTypeCode() == 1 and prev.quotes.open > current.quotes.close and prev.quotes.close < current.quotes.open:
            return CombinationType(7) #包み線
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getThreeTypeCode() == 2 and prev.quotes.open < current.quotes.close and prev.quotes.close > current.quotes.open:
            return CombinationType(7) #包み線
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getThreeTypeCode() == 2 and prev.quotes.open > current.quotes.close and prev.quotes.close < current.quotes.open:
            return CombinationType(8) #はらみ線
        if prev.candleStick.getThreeTypeCode() == 2 and current.candleStick.getThreeTypeCode() == 1 and prev.quotes.open < current.quotes.close and prev.quotes.close > current.quotes.open:
            return CombinationType(8) #はらみ線
        if prev.candleStick.getNineTypeCode() == 2 and current.candleStick.getNineTypeCode() == 3 and (prev.quotes.close*CommonPackage.blankCoefficient) < current.quotes.close:
            return CombinationType(9) #星
        if prev.candleStick.getThreeTypeCode() == 2 and current.candleStick.getThreeTypeCode() == 2 and prev.quotes.open == current.quotes.open:
            return CombinationType(12) #並び赤
        if prev.candleStick.getThreeTypeCode() == 1 and current.candleStick.getThreeTypeCode() == 1 and prev.quotes.open == current.quotes.open:
            return CombinationType(13) #並び黒
        if prev.quotes.close == current.quotes.close:
            return CombinationType(10) #出合い線
        if prev.quotes.open == current.quotes.open:
            return CombinationType(11) #行き違い線
        return CombinationType(0)