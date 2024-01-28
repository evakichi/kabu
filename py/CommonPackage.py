import requests
import os
import json
import datetime
import Data
import math
import numpy as np

homeDir = os.environ.get('HOME')
dataDir=os.path.join(homeDir,'quants_data')
bigSmallThreshold = 1.3
numOfThreads = 1

def getNextInterIter(size,current,numOfThreads):
    if math.ceil(size/numOfThreads) != math.floor(size/numOfThreads) and current == math.floor(size/numOfThreads):
        return size % numOfThreads
    return numOfThreads

def getTokens()-> (str,str):
    mail = os.environ.get('J_QUANTS_MAIL_ADDRESS')
    passwd = os.environ.get('J_QUANTS_PASSWD')

    data={"mailaddress":mail, "password":passwd}
    refreshToken_post = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
    refreshToken_json = refreshToken_post.json()
    refreshToken = refreshToken_json['refreshToken']
    print(refreshToken)
    idToken_post = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refreshToken}")
    idToken_json = idToken_post.json()
    idToken = idToken_json['idToken']
    print(idToken)

    return refreshToken,idToken

def getDates(fromDistance,toDistance) -> (str,str):
    current_datetime = datetime.datetime.today()

    fromDate = current_datetime + datetime.timedelta(days=-1*fromDistance)
    toDate = current_datetime + datetime.timedelta(days=-1*toDistance)

    return fromDate.strftime('%Y%m%d'),toDate.strftime('%Y%m%d')

def getBrandInfo(idToken):
    headers = {'Authorization': 'Bearer {}'.format(idToken)}
    information_get = requests.get(f"https://api.jquants.com/v1/listed/info", headers=headers)
    information_json = information_get.json()
    return information_json['info']
    
def createDir(path) -> str:
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def getNextThreadSize(currentVolume,numOfThreads)->int:
    pass
    return 0

def isNone(openVal,highVal,lowVal,closeVal):
   if openVal != None and highVal != None and lowVal != None and closeVal != None:
       return False
   return True
 
def isAsce(data0,data1):
    if data0.max() < data1.max():
        return True
    return False    

def isDesc(data0,data1):
    if data0.min() > data1.min():
        return True
    return False    

def isFlat(data0,data1):
    if data0.max() == data1.max() and data0.min() == data1.min():
        return True
    return False    

def existsWindow(data0,data1):
    if data0.min() > data1.max()*1.05:
        return True
    if data0.max()*1.05 < data1.min():
        return True
    return False

def getPastDays(worksheet,current,days):

    pastDays = list()
    
    for d in range(days,-1,-1):
        pastDays.append(Data.Data(worksheet[f'B{current - d}'].value,
                                  worksheet[f'C{current - d}'].value,
                                  worksheet[f'D{current - d}'].value,
                                  worksheet[f'E{current - d}'].value))
    return pastDays

def pattern050000(data,count,debug=False): #三空叩き込み
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].hasWindow()           and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].hasWindow()           and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].hasWindow()           and \
        data[count + 3].isNegative()      and data[count + 4].isAsce()   and data[count + 4].dontCare()            and \
        data[count + 4].dontCare()        :

        data[count + 4].appendAnalysisData(0)
#        if debug:
#            print(data[count + 4].getAnalysisData().getAnalyzedDataStrings())

def pattern050100(data,count,debug=False): #三手大陰線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isBigNegative()   and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].dontCare()            and \
        data[count + 3].isBigNegative()   and data[count + 4].isDesc()   and data[count + 4].dontCare()            and \
        data[count + 4].dontCare()        :

        data[count + 4].appendAnalysisData(1)
#        if debug:
#            print(data[count + 4].getAnalysisData().getAnalyzedDataStrings())

def pattern050200(data,count,debug=False): #最後の抱き陰線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()            and \
        data[count + 3].isPositive()      and data[count + 4].dontCare() and data[count + 4].isIncludePrev()         and \
        data[count + 4].isBigNegative()   :

        data[count + 4].appendAnalysisData(2)
#        if debug:
#            print(data[count + 4].getAnalysisData().getAnalyzedDataStrings())

def pattern060300(data,count,debug=False): #明けの明星
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].hasWindow()           and \
        data[count + 4].isPositive()      and data[count + 5].isAsce()   and data[count + 5].dontCare()            and \
        data[count + 5].isPositive()      :

        data[count + 5].appendAnalysisData(3)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern060400(data,count,debug=False): #捨て子底
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].hasWindow()           and \
        data[count + 3].isCross()         and data[count + 4].isAsce()   and data[count + 4].hasWindow()           and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()            and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(4)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern060500(data,count,debug=False): #大陰線のはらみ寄せ
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isBigNegative()   and data[count + 3].dontCare() and data[count + 3].isIncludedFromPrev()   and \
        data[count + 3].isCross()         and data[count + 4].isAsce()   and data[count + 4].isIncludePrev()        and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(5)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern060600(data,count,debug=False): #たくり線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].hasWindow()            and \
        data[count + 3].isNegative()      and data[count + 4].isAsce()   and data[count + 4].getCandleState() == 19 and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(6)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern060700(data,count,debug=False): #勢力線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].hasWindow()            and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].getCandleState() == 9  and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(7)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern060800(data,count,debug=False): #陰の陰はらみ
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].isIncludedFromPrev()     and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].dontCare()             and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(8)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern070900(data,count,debug=False): #放れ五手黒一本底
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].hasWindow()            and \
        data[count + 1].isSmall()         and data[count + 2].isDesc()   and data[count + 2].isClose()              and \
        data[count + 2].isSmall()         and data[count + 3].dontCare() and data[count + 3].isClose()              and \
        data[count + 3].isSmall()         and data[count + 4].dontCare() and data[count + 4].isClose()              and \
        data[count + 4].isSmall()         and data[count + 5].isAsce()   and data[count + 5].hasWindow()            and \
        data[count + 5].bigNegative()     and data[count + 6].dontCare() and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(9)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern071000(data,count,debug=False): #やぐら底
    if  data[count + 0].isBigNegative()   and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isSmall()         and data[count + 2].dontCare() and data[count + 2].isClose()              and \
        data[count + 2].isSmall()         and data[count + 3].dontCare() and data[count + 3].isClose()              and \
        data[count + 3].isSmall()         and data[count + 4].dontCare() and data[count + 4].isClose()              and \
        data[count + 4].isSmall()         and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].isBigPositive()   and data[count + 6].isAsce()   and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(10)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern071100(data,count,debug=False): #小幅上放れ黒線
    if  data[count + 0].isNegative()   and data[count + 1].dontCare() and data[count + 1].isClose()              and \
        data[count + 1].isPositive()   and data[count + 2].dontCare() and data[count + 2].isClose()              and \
        data[count + 2].isNegative()   and data[count + 3].dontCare() and data[count + 3].isClose()              and \
        data[count + 3].isPositive()   and data[count + 4].dontCare() and data[count + 4].isClose()              and \
        data[count + 4].isNegative()   and data[count + 5].isAsce()   and data[count + 5].hasWindow()            and \
        data[count + 5].isNegative()   and data[count + 6].isAsce()   and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(11)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern061200(data,count,debug=False): #放れ七手の変化底
    if  data[count + 0].isNegative()   and data[count + 1].isDesc()   and data[count + 1].hasWindow()            and \
        data[count + 1].isSmall()      and data[count + 2].dontCare() and data[count + 2].isClose()              and \
        data[count + 2].isSmall()      and data[count + 3].dontCare() and data[count + 3].isClose()              and \
        data[count + 3].isSmall()      and data[count + 4].dontCare() and data[count + 4].isClose()              and \
        data[count + 4].isSmall()      and data[count + 5].isAsce()   and data[count + 5].hasWindow()            and \
        data[count + 5].isPositive()   :

        data[count + 5].appendAnalysisData(12)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern061300(data,count,debug=False): #連続下げ放れ三つ星
    if  data[count + 0].isNegative()   and data[count + 1].isDesc()   and data[count + 1].hasWindow()            and \
        data[count + 1].isSmall()      and data[count + 2].dontCare() and data[count + 2].isClose()              and \
        data[count + 2].isSmall()      and data[count + 3].dontCare() and data[count + 3].isClose()              and \
        data[count + 3].isSmall()      and data[count + 4].dontCare() and data[count + 4].isClose()              and \
        data[count + 4].isCross()      and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].isPositive()   :

        data[count + 5].appendAnalysisData(13)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern061400(data,count,debug=False): #逆襲線
    if  data[count + 0].isNegative()    and data[count + 1].isDesc()   and data[count + 1].isClose()              and \
        data[count + 1].isNegative()    and data[count + 2].isDesc()   and data[count + 2].isClose()              and \
        data[count + 2].isNegative()    and data[count + 3].isDesc()   and data[count + 3].hasWindow()            and \
        data[count + 3].isBigPositive() and data[count + 4].isAsce()   and data[count + 4].isClose()              and \
        data[count + 4].dontCare()      and data[count + 5].isAsce()   and data[count + 5].isClose()              and \
        data[count + 5].dontCare()      :

        data[count + 5].appendAnalysisData(14)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())
6
def pattern061500(data,count,debug=False): #抱き陽線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isSmallNegative() and data[count + 4].dontCare() and data[count + 4].isIncludePrev()          and \
        data[count + 4].isBigPositive()   and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(15)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern061600(data,count,debug=False): #寄り切り陽線
    if  data[count + 0].isSmall()       and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isSmall()       and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isSmall()       and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isSmall()       and data[count + 4].dontCare() and (data[count + 4].getCandleState() == 2 or data[count + 4].getCandleState() == 4)            and \
        data[count + 4].isPositive()    and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(16)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern071700(data,count,debug=False): #赤三兵
    if  data[count + 0].isSmallNegative() and data[count + 1].dontCare() and data[count + 1].dontCare()             and \
        data[count + 1].isSmallNegative() and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isSmallNegative() and data[count + 3].dontCare() and data[count + 3].dontCare()             and \
        data[count + 3].isSmallPositive() and data[count + 4].isAsce()   and data[count + 4].dontCare()             and \
        data[count + 4].isSmallPositive() and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].isSmallPositive() and data[count + 6].isAsce()   and data[count + 6].hasWindow()            and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(17)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern071800(data,count,debug=False): #下位の陽線五本
    if  data[count + 0].isNegative()      and data[count + 1].dontCare() and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isPositive()      and data[count + 3].dontCare() and data[count + 3].dontCare()             and \
        data[count + 3].isPositive()      and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].isPositive()      and data[count + 5].dontCare() and data[count + 5].dontCare()             and \
        data[count + 5].isPositive()      and data[count + 6].dontCare() and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(18)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern071900(data,count,debug=False): #押え込み線
    if  data[count + 0].isPositive()      and data[count + 1].dontCare() and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isNegative()      and data[count + 4].isDesc()   and data[count + 4].dontCare()             and \
        data[count + 4].isNegative()      and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].isPositive()      and data[count + 6].dontCare() and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(19)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern072000(data,count,debug=False): #上げの差し込み線
    if  data[count + 0].isPositive()      and data[count + 1].dontCare() and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].dontCare()             and \
        data[count + 3].isNegative()      and data[count + 4].isDesc()   and data[count + 4].dontCare()             and \
        data[count + 4].isPositive()      and data[count + 5].dontCare() and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        and data[count + 6].dontCare() and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(20)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern062100(data,count,debug=False): #上げ三法
    if  data[count + 0].isPositive()      and data[count + 1].dontCare() and data[count + 1].dontCare()             and \
        data[count + 1].isBigPositive()   and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isNegative()      and data[count + 4].isDesc()   and data[count + 4].dontCare()             and \
        data[count + 4].isNegative()      and data[count + 5].dontCare() and data[count + 5].dontCare()             and \
        data[count + 5].isBigPositive()   :

        data[count + 5].appendAnalysisData(21)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern062200(data,count,debug=False): #カブセの上抜け
    if  data[count + 0].isPositive()      and data[count + 1].dontCare() and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isNegative()      and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].isPositive()      and data[count + 5].dontCare() and data[count + 5].dontCare()             and \
        data[count + 5].isBigPositive()   :

        data[count + 5].appendAnalysisData(22)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern062300(data,count,debug=False): #上伸途上の連続タスキ
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].dontCare()             and \
        data[count + 2].isPositive()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isNegative()      and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].dontCare()        and data[count + 5].dontCare() and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :
    
        data[count + 5].appendAnalysisData(23)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern062400(data,count,debug=False): #上放れタスキ
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].hasWindow()            and \
        data[count + 2].isPositive()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isNegative()      and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].dontCare()        and data[count + 5].dontCare() and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(24)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern062500(data,count,debug=False): #上伸途上のクロス
    if  data[count + 0].isPositive()      and data[count + 1].dontCare()   and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].dontCare()   and data[count + 2].dontCare()            and \
        data[count + 2].isPositive()      and data[count + 3].isDesc()     and data[count + 3].dontCare()             and \
        data[count + 3].isBigPositive()   and data[count + 4].dontCare()   and data[count + 4].dontCare()             and \
        data[count + 4].isCross()         and data[count + 5].dontCare()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(25)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern062600(data,count,debug=False): #上げの三つ星
    if  data[count + 0].isPositive()      and data[count + 1].dontCare()   and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].dontCare()   and data[count + 2].dontCare()             and \
        data[count + 2].isSmall()         and data[count + 3].dontCare()   and data[count + 3].dontCare()             and \
        data[count + 3].isSmall()         and data[count + 4].dontCare()   and data[count + 4].dontCare()             and \
        data[count + 4].isSmall()         and data[count + 5].dontCare()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(26)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern072700(data,count,debug=False): #並び赤
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()     and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()     and data[count + 2].dontCare()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()     and data[count + 3].hasWindow()            and \
        data[count + 3].isPositive()      and data[count + 4].isFlat()     and data[count + 4].isClose()              and \
        data[count + 4].isPositive()      and data[count + 5].dontCare()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        and data[count + 5].dontCare()   and data[count + 5].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(27)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern072800(data,count,debug=False): #上放れ陰線二本連続
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()     and data[count + 1].hasWindow()            and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()     and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isAsce()     and data[count + 3].dontCare()             and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()     and data[count + 4].dontCare()             and \
        data[count + 4].isPositive()      and data[count + 5].isAsce()     and data[count + 5].hasWindow()            and \
        data[count + 5].isNegative()      and data[count + 5].isDesc()     and data[count + 5].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].appendAnalysisData(28)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern072900(data,count,debug=False): #上位の連続大陽線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()     and data[count + 1].isClose()              and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()     and data[count + 2].isClose()              and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()     and data[count + 3].isClose()              and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()     and data[count + 4].isClose()              and \
        data[count + 4].isBigPositive()   and data[count + 5].isAsce()     and data[count + 5].isClose()              and \
        data[count + 5].isBigPositive()   and data[count + 5].isAsce()     and data[count + 5].isClose()              and \
        data[count + 6].isBigPositive()   :

        data[count + 6].appendAnalysisData(29)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern063000(data,count,debug=False): #波高い線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()     and data[count + 1].isClose()              and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()     and data[count + 2].isClose()              and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()     and data[count + 3].isClose()              and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()     and data[count + 4].isClose()              and \
        data[count + 4].isPositive()      and data[count + 5].dontCare()   and data[count + 5].isClose()              and \
        data[count + 5].dontCare()        and \
        data[count + 3].getHigh() > data[count + 3].getClose()*1.1 and data[count + 3].getLow() < data[count + 4].getOpen() and data[count + 3].getHigh() > data[count + 4].getClose():

        data[count + 5].appendAnalysisData(30)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern053100(data,count,debug=False): #三空踏み上げ
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].hasWindow()           and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].hasWindow()           and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isDesc()   and data[count + 4].dontCare()            and \
        data[count + 4].dontCare()        :

        data[count + 4].appendAnalysisData(31)
#        if debug:
#            print(data[count + 4].getAnalysisData().getAnalyzedDataStrings())

def pattern083200(data,count,debug=False): #新値八手利食い線
    if  data[count + 0].dontCare()        and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].dontCare()        and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].dontCare()        and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].dontCare()        and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        and data[count + 6].isAsce()   and data[count + 6].isClose()             and \
        data[count + 6].dontCare()        and data[count + 7].isAsce()   and data[count + 7].isClose()             and \
        data[count + 7].dontCare()        :

        data[count + 7].appendAnalysisData(32)
#        if debug:
#            print(data[count + 7].getAnalysisData().getAnalyzedDataStrings())

def pattern053300(data,count,debug=False): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isCross()         :

        data[count + 4].appendAnalysisData(33)
#        if debug:
#            print(data[count + 4].getAnalysisData().getAnalyzedDataStrings())

def pattern063301(data,count,debug=False): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].isAsce()   and data[count + 5].isClose()             and \
        data[count + 5].isCross()         :

        data[count + 5].appendAnalysisData(33)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern073302(data,count,debug=False): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].isAsce()   and data[count + 5].isClose()             and \
        data[count + 5].isPositive()      and data[count + 6].isAsce()   and data[count + 6].isClose()             and \
        data[count + 6].isCross()         :

        data[count + 6].appendAnalysisData(33)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern083303(data,count,debug=False): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].isAsce()   and data[count + 5].isClose()             and \
        data[count + 5].isPositive()      and data[count + 6].isAsce()   and data[count + 6].isClose()             and \
        data[count + 6].isPositive()      and data[count + 7].isAsce()   and data[count + 7].isClose()             and \
        data[count + 7].isCross()         :

        data[count + 7].appendAnalysisData(33)
#        if debug:
#            print(data[count + 7].getAnalysisData().getAnalyzedDataStrings())

def pattern063400(data,count,debug=False): #行き詰まり線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].dontCare()            and \
        data[count + 3].isBigPositive()   and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        and \
        data[count + 3].getHigh() > data[count + 3].getClose()*1.10 :

        data[count + 5].appendAnalysisData(34)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern063500(data,count,debug=False): #三羽ガラス
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isDesc()   and data[count + 3].isClose()             and \
        data[count + 3].isNegative()      and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].isNegative()      and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].isNegative()         :

        data[count + 5].appendAnalysisData(35)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern063600(data,count,debug=False): #首吊り線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].hasWindow()           and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].isPositive()      and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].dontCare()        and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        and \
        data[count + 3].getLow()*1.10 < data[count + 3].getOpen() :

        data[count + 5].appendAnalysisData(36)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern063700(data,count,debug=False): #上位の上放れ陰線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].hasWindow()           and \
        data[count + 4].isNegative()      and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(37)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern063800(data,count,debug=False): #宵の明星
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isDesc()   and data[count + 4].hasWindow()           and \
        data[count + 4].isNegative()      and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(38)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern063900(data,count,debug=False): #陽の陽はらみ
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isBigPositive()   and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].isPositive()      and data[count + 4].isDesc()   and data[count + 4].isIncludedFromPrev()    and \
        data[count + 4].dontCare()        and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(39)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern064000(data,count,debug=False): #最後の抱き陽線
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].isNegative()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].isDesc()   and data[count + 5].isIncludedPrev()        and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(40)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern084100(data,count,debug=False): #抱き陽線
    if  data[count + 0].dontCare()        and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].dontCare()        and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].dontCare()        and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].dontCare()        and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].dontCare() and data[count + 5].isIncludedPrev()        and \
        data[count + 5].isNegative()      and data[count + 6].isDesc()   and data[count + 6].isClose()             and \
        data[count + 6].dontCare()        and data[count + 7].isDesc()   and data[count + 7].isClose()             and \
        data[count + 7].dontCare()        :

        data[count + 7].appendAnalysisData(41)
#        if debug:
#            print(data[count + 7].getAnalysisData().getAnalyzedDataStrings())

def pattern084200(data,count,debug=False): #つたい線の打ち返し
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].isPositive()      and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].isNegative()      and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].isNegative()      and data[count + 6].isAsce()   and data[count + 6].isClose()             and \
        data[count + 6].isBigPositive()   and data[count + 7].isDesc()   and data[count + 7].isClose()             and \
        data[count + 7].dontCare()        :

        data[count + 7].appendAnalysisData(42)
#        if debug:
#            print(data[count + 7].getAnalysisData().getAnalyzedDataStrings())

def pattern084300(data,count,debug=False): #放れ五手赤一本
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].dontCare()        and data[count + 3].isAsce()   and data[count + 3].hasWindow()           and \
        data[count + 3].dontCare()        and data[count + 4].dontCare() and data[count + 4].isClose()             and \
        data[count + 4].dontCare()        and data[count + 5].dontCare() and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        and data[count + 6].isAsce()   and data[count + 6].isClose()             and \
        data[count + 6].isBigPositive()   and data[count + 7].isDesc()   and data[count + 7].isClose()             and \
        data[count + 7].dontCare()        :

        data[count + 7].appendAnalysisData(43)
#        if debug:
#            print(data[count + 7].getAnalysisData().getAnalyzedDataStrings())

def pattern084400(data,count,debug=False): #放れ七手大黒
    if  data[count + 0].isPositive()      and data[count + 1].isAsce()   and data[count + 1].hasWindow()           and \
        data[count + 1].isBigPositive()   and data[count + 2].dontCare() and data[count + 2].isClose()             and \
        data[count + 2].dontCare()        and data[count + 3].dontCare() and data[count + 3].isClose()             and \
        data[count + 3].dontCare()        and data[count + 4].dontCare() and data[count + 4].isClose()             and \
        data[count + 4].dontCare()        and data[count + 5].dontCare() and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        and data[count + 6].dontCare() and data[count + 6].isClose()             and \
        data[count + 6].dontCare()        and data[count + 7].dontCare() and data[count + 7].isClose()             and \
        data[count + 7].isBigNegative()        :

        data[count + 7].appendAnalysisData(44)
#        if debug:
#            print(data[count + 7].getAnalysisData().getAnalyzedDataStrings())

def pattern054500(data,count,debug=False): #差し込み線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].isClose()             and \
        data[count + 3].isPositive()      and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].dontCare()         :

        data[count + 4].appendAnalysisData(45)
#        if debug:
#            print(data[count + 4].getAnalysisData().getAnalyzedDataStrings())

def pattern074600(data,count,debug=False): #下放れ三手
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].hasWindow()           and \
        data[count + 2].isPositive()      and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].dontCare() and data[count + 5].isClose()             and \
        data[count + 5].isNegative()      and data[count + 6].isDesc()   and data[count + 6].isClose()             and \
        data[count + 6].dontCare()         :

        data[count + 6].appendAnalysisData(46)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern074700(data,count,debug=False): #下げ三法
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].isClose()             and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isPositive()      and data[count + 5].isAsce()   and data[count + 5].isClose()             and \
        data[count + 5].isPositive()      and data[count + 6].isDesc()   and data[count + 6].isClose()             and \
        data[count + 6].isNegative()         :

        data[count + 6].appendAnalysisData(47)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern074800(data,count,debug=False): #三手打ち
    if  data[count + 0].isNegative()      and data[count + 1].dontCare() and data[count + 1].isClose()             and \
        data[count + 1].isPositive()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].isClose()             and \
        data[count + 3].isNegative()      and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].isNegative()      and data[count + 5].dontCare() and data[count + 5].isClose()             and \
        data[count + 5].isBigPositive()   and data[count + 6].dontCare() and data[count + 6].isClose()             and \
        data[count + 6].isCross()         :

        data[count + 6].appendAnalysisData(48)
#        if debug:
#            print(data[count + 6].getAnalysisData().getAnalyzedDataStrings())

def pattern054900(data,count,debug=False): #下落途上の連続タスキ
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isNegative()      and data[count + 3].isAsce()   and data[count + 3].isClose()           and \
        data[count + 3].isPositive()      and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].dontCare()         :

        data[count + 4].appendAnalysisData(49)
#        if debug:
#            print(data[count + 4].getAnalysisData().getAnalyzedDataStrings())

def pattern065000(data,count,debug=False): #化け線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].isClose()             and \
        data[count + 3].isNegative()      and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isBigPositive()   and data[count + 5].dontCare() and data[count + 5].isClose()             and \
        data[count + 5].isCross()         :

        data[count + 5].appendAnalysisData(50)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern065100(data,count,debug=False): #下げ足のクロス
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].isClose()             and \
        data[count + 3].isCross()         and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].dontCare()        and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(51)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern065200(data,count,debug=False): #下放れ黒二本
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].hasWindow()           and \
        data[count + 3].isNegative()      and data[count + 4].dontCare() and data[count + 4].isClose()             and \
        data[count + 4].isNegative()      and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()         :

        data[count + 5].appendAnalysisData(52)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern065300(data,count,debug=False): #下げの三つ星
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isSmallNegative() and data[count + 3].isAsce()   and data[count + 3].isClose()             and \
        data[count + 3].isSmallPositive() and data[count + 4].isAsce()   and data[count + 4].isClose()             and \
        data[count + 4].isSmallPositive() and data[count + 5].isAsce()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        :

        data[count + 5].appendAnalysisData(53)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern065400(data,count,debug=False): #上位の陰線五本
    if  data[count + 0].isBigPositive()   and data[count + 1].dontCare() and data[count + 1].isClose()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].isClose()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].isClose()             and \
        data[count + 3].isNegative()      and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].isNegative()      and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].isNegative()         :

        data[count + 5].appendAnalysisData(54)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())

def pattern065500(data,count,debug=False): #寄り切り陰線
    if  data[count + 0].isSmall()         and data[count + 1].isAsce()   and data[count + 1].isClose()             and \
        data[count + 1].isSmall()         and data[count + 2].isAsce()   and data[count + 2].isClose()             and \
        data[count + 2].isSmall()         and data[count + 3].isAsce()   and data[count + 3].isClose()           and \
        data[count + 3].isSmall()         and data[count + 4].isDesc()   and data[count + 4].isClose()             and \
        data[count + 4].isBigNegative()   and data[count + 5].isDesc()   and data[count + 5].isClose()             and \
        data[count + 5].dontCare()        and \
        data[count + 4].getCandleState() == 12 and data[count + 4].getCandleState() == 13 :

        data[count + 5].appendAnalysisData(55)
#        if debug:
#            print(data[count + 5].getAnalysisData().getAnalyzedDataStrings())




