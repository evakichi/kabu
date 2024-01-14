import requests
import os
import json
import datetime
import Data
import math
import numpy as np

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

def pattern0000(data,count,debug=False): #三空叩き込み
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].hasWindow()           and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].hasWindow()           and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].hasWindow()           and \
        data[count + 3].isNegative()      and data[count + 4].isAsce()   and data[count + 4].dontCare()            and \
        data[count + 4].dontCare()        :

        data[count + 4].set5RowsStatus(0)
        if debug:
            print(data[count + 4].get5RowsStatus().getAnzlyzedDataString())

def pattern0100(data,count,debug=False): #三手大陰線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isBigNegative()   and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].dontCare()            and \
        data[count + 3].isBigNegative()   and data[count + 4].isDesc()   and data[count + 4].dontCare()            and \
        data[count + 4].dontCare()        :

        data[count + 4].set5RowsStatus(0)
        if debug:
            print(data[count + 4].get5RowsStatus().getAnzlyzedDataString())

def pattern0200(data,count,debug=False): #最後の抱き陰線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()            and \
        data[count + 3].isPositive()      and data[count + 4].dontCare() and data[count + 4].includePrev()         and \
        data[count + 4].isBigNegative()   :

        data[count + 4].set5RowsStatus(0)
        if debug:
            print(data[count + 4].get5RowsStatus().getAnzlyzedDataString())

def pattern0300(data,count,debug=False): #明けの明星
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].hasWindow()           and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].hasWindow()           and \
        data[count + 4].isPositive()      and data[count + 5].isAsce()   and data[count + 5].dontCare()            and \
        data[count + 5].isPositive()      :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern0400(data,count,debug=False): #捨て子底
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()            and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()            and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].hasWindow()           and \
        data[count + 3].isCross()         and data[count + 4].isAsce()   and data[count + 4].hasWindow()           and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()            and \
        data[count + 5].dontCare()        :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern0500(data,count,debug=False): #大陰線のはらみ寄せ
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isBigNegative()   and data[count + 3].dontCare() and data[count + 3].isIncludedFromPrev()   and \
        data[count + 3].isCross()         and data[count + 4].isAsce()   and data[count + 4].isIncludePrev()        and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern0600(data,count,debug=False): #たくり線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].hasWindow()            and \
        data[count + 3].isNegative()      and data[count + 4].isAsce()   and data[count + 4].getCandleState() == 19 and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern0700(data,count,debug=False): #勢力線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].hasWindow()            and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].getCandleState() == 9  and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern0800(data,count,debug=False): #陰の陰はらみ
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isBigNegative()   and data[count + 3].isDesc()   and data[count + 3].includedFromPrev()     and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].dontCare()             and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern0900(data,count,debug=False): #放れ五手黒一本底
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isPositive()      and data[count + 4].isAsce()   and data[count + 4].dontCare()             and \
        data[count + 4].isNegative()      and data[count + 5].isAsce()   and data[count + 5].hasWindow()            and \
        data[count + 5].bigNegative()     and data[count + 6].isAsce()   and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].set7RowsStatus(0)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern1000(data,count,debug=False): #やぐら底
    if  data[count + 0].isBigNegative()   and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].dontCare()        and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].dontCare()        and data[count + 3].dontCare() and data[count + 3].dontCare()             and \
        data[count + 3].dontCare()        and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].dontCare()        and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].isBigPositive()   and data[count + 6].isAsce()   and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].set7RowsStatus(0)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern1100(data,count,debug=False): #小幅上放れ黒線
    if  data[count + 0].isNegative()   and data[count + 1].dontCare() and data[count + 1].dontCare()             and \
        data[count + 1].isPositive()   and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()   and data[count + 3].dontCare() and data[count + 3].dontCare()             and \
        data[count + 3].isPositive()   and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].isNegative()   and data[count + 5].isAsce()   and data[count + 5].hasWindow()            and \
        data[count + 5].isNegative()   and data[count + 6].isAsce()   and data[count + 6].dontCare()             and \
        data[count + 6].dontCare()        :

        data[count + 6].set7RowsStatus(0)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern1200(data,count,debug=False): #放れ七手の変化底
    if  data[count + 0].isNegative()   and data[count + 1].isDesc()   and data[count + 1].hasWindow()             and \
        data[count + 1].isSmall()      and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isSmall()      and data[count + 3].dontCare() and data[count + 3].dontCare()             and \
        data[count + 3].isSmall()      and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].isSmall()      and data[count + 5].isAsce()   and data[count + 5].hasWindow()            and \
        data[count + 5].isPositive()   :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern1300(data,count,debug=False): #連続下げ放れ三つ星
    if  data[count + 0].isNegative()   and data[count + 1].isDesc()   and data[count + 1].hasWindow()            and \
        data[count + 1].isSmall()      and data[count + 2].dontCare() and data[count + 2].dontCare()             and \
        data[count + 2].isSmall()      and data[count + 3].dontCare() and data[count + 3].dontCare()             and \
        data[count + 3].isSmall()      and data[count + 4].dontCare() and data[count + 4].dontCare()             and \
        data[count + 4].isCross()      and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].isPositive()   :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern1400(data,count,debug=False): #逆襲線
    if  data[count + 0].isNegative()    and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()    and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()    and data[count + 3].isDesc()   and data[count + 3].hasWindow()            and \
        data[count + 3].isBigPositive() and data[count + 4].isAsce()   and data[count + 4].dontCare()             and \
        data[count + 4].dontCare()      and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()      :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern1500(data,count,debug=False): #抱き陽線
    if  data[count + 0].isNegative()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].isNegative()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].isNegative()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].isSmallNegative() and data[count + 4].dontCare() and data[count + 4].includePrev()          and \
        data[count + 4].isBigPositive()   and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern1600(data,count,debug=False): #寄り切り陽線
    if  data[count + 0].dontCare()      and data[count + 1].isDesc()   and data[count + 1].dontCare()             and \
        data[count + 1].dontCare()      and data[count + 2].isDesc()   and data[count + 2].dontCare()             and \
        data[count + 2].dontCare()      and data[count + 3].isDesc()   and data[count + 3].dontCare()             and \
        data[count + 3].dontCare()      and data[count + 4].dontCare() and (data[count + 4].getCandleState() == 2 or data[count + 4].getCandleState() == 4)            and \
        data[count + 4].isPositive()    and data[count + 5].isAsce()   and data[count + 5].dontCare()             and \
        data[count + 5].dontCare()        :

        data[count + 5].set6RowsStatus(0)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern1700(data,count,debug=False): #赤三兵
    if  data[count + 0].isSmallNegative() and \
        data[count + 1].isSmallNegative() and \
        data[count + 2].isSmallNegative() and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallPositive() and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isSmallPositive() and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isSmallPositive() and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7RowsStatus(17)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern1800(data,count,debug=False): #下位の陽線五本
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7RowsStatus(18)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern1900(data,count,debug=False): #押え込み線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7RowsStatus(19)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern2000(data,count,debug=False): #上げの差し込み線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7RowsStatus(20)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern2100(data,count,debug=False): #上げ三法
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive()   and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive():

        data[count + 5].set6RowsStatus(21)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern2200(data,count,debug=False): #カブセの上抜け
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6RowsStatus(22)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern2300(data,count,debug=False): #上伸途上の連続タスキ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6RowsStatus(23)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern2400(data,count,debug=False): #上放れタスキ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6RowsStatus(24)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern2500(data,count,debug=False): #上伸途上のクロス
    if  data[count + 0].isPositive()      and \
        data[count + 1].isPositive()      and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isBigPositive()   and \
        data[count + 4].isCross()         and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6RowsStatus(25)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern2600(data,count,debug=False): #上げの三つ星
    if  data[count + 0].isPositive()      and \
        data[count + 1].isPositive()      and \
        data[count + 2].isSmallNegative() and \
        data[count + 3].isSmallPositive() and \
        data[count + 4].isSmallNegative() and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6RowsStatus(26)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern2700(data,count,debug=False): #並び赤
    if  data[count + 0].isPositive()      and \
        data[count + 1].isPositive()      and \
        data[count + 2].isPositive()      and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallPositive() and \
        data[count + 4].isSmallPositive() and isAsce(data[count + 4],data[count + 5]) and \
        isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7RowsStatus(27)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern2800(data,count,debug=False): #上放れ陰線二本連続
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative()      and isDesc(data[count + 5],data[count + 6]) :

        data[count + 6].set7RowsStatus(28)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern2900(data,count,debug=False): #上位の連続大陽線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isAsce(data[count + 4],data[count + 5]) and \
        existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 5].isBigPositive()   and isAsce(data[count + 5],data[count + 6]) and \
        data[count + 6].isBigPositive():

        data[count + 6].set7RowsStatus(29)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern3000(data,count,debug=False): #波高い線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 3].getClose()*1.10 < data[count + 4].getHigh() and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]):
        
        data[count + 5].set6RowsStatus(30)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern3100(data,count,debug=False): #三空踏み上げ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]):
        
        data[count + 4].set5RowsStatus(31)
        if debug:
            print(data[count + 4].get5RowsStatus().getAnzlyzedDataString())

def pattern3200(data,count,debug=False): #新値八手利食い線
    if  data[count + 0].max() < data[count + 1].max() < data[count + 2].max() < data[count + 3].max() < \
        data[count + 4].max() < data[count + 4].max() < data[count + 6].max() < data[count + 7].max():
        
        data[count + 7].set8RowsStatus(32)
        if debug:
            print(data[count + 7].get8RowsStatus().getAnzlyzedDataString())

def pattern3300(data,count,debug=False): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 4].isCross():
        
        data[count + 4].set5RowsStatus(33)
        if debug:
            print(data[count + 5].get5RowsStatus().getAnzlyzedDataString())

def pattern3301(data,count,debug=False): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isCross():
        
        data[count + 5].set6RowsStatus(33)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern3302(data,count,debug=False): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]) and \
        data[count + 6].isCross():
        
        data[count + 6].set7RowsStatus(33)
        if debug:
            print(data[count + 5].get7RowsStatus().getAnzlyzedDataString())

def pattern3400(data,count,debug=False): #行き詰まり線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isBigPositive()   and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 3].getHigh() > data[count].getClose()*1.10:
        
        data[count + 5].set6RowsStatus(34)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern3500(data,count,debug=False): #三羽ガラス
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative() and \
        data[count + 3].getClose() < data[count + 4].getOpen() and \
        data[count + 4].getClose() < data[count + 5].getOpen():
        
        data[count + 5].set6RowsStatus(35)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern3600(data,count,debug=False): #首吊り線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].getLow() < data[count + 3].getOpen()*0.90 and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]) and \
        isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6RowsStatus(36)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern3700(data,count,debug=False): #上位の上放れ陰線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6RowsStatus(37)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern3800(data,count,debug=False): #宵の明星
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]) and \
        existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6RowsStatus(38)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern3900(data,count,debug=False): #陽の陽はらみ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 3].getClose()  > data[count + 4].getClose() and \
        data[count + 3].getOpen() < data[count + 4].getOpen() and \
        isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6RowsStatus(39)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern4000(data,count,debug=False): #最後の抱き陽線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 3].getOpen()  < data[count + 4].getClose() and \
        data[count + 3].getClose() > data[count + 4].getOpen():
        
        data[count + 5].set6RowsStatus(40)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern4100(data,count,debug=False): #抱き陽線
    if  isAsce(data[count + 0],data[count + 1]) and \
        isAsce(data[count + 1],data[count + 2]) and \
        isAsce(data[count + 2],data[count + 3]) and \
        isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]) and \
        data[count + 4].isBigNegative() and isDesc(data[count + 5],data[count + 6]) and \
        isDesc(data[count + 6],data[count + 7]) and \
        data[count + 4].getOpen()  > data[count + 5].getClose() and \
        data[count + 4].getClose() < data[count + 5].getOpen():
        
        data[count + 7].set8RowsStatus(41)
        if debug:
            print(data[count + 7].get8RowsStatus().getAnzlyzedDataString())

def pattern4200(data,count,debug=False): #つたい線の打ち返し
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()    and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()    and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()    and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()    and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative()    and isAsce(data[count + 5],data[count + 6]) and \
        data[count + 6].isBigPositive() and isDesc(data[count + 6],data[count + 7]):
        
        data[count + 7].set8RowsStatus(42)
        if debug:
            print(data[count + 7].get8RowsStatus().getAnzlyzedDataString())

def pattern4300(data,count,debug=False): #放れ五手赤一本
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()    and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()    and \
        data[count + 3].isNegative()    and \
        data[count + 4].isPositive()    and \
        data[count + 5].isNegative()    and \
        data[count + 6].isBigPositive() and isDesc(data[count + 6],data[count + 7]):
        
        data[count + 7].set8RowsStatus(43)
        if debug:
            print(data[count + 7].get8RowsStatus().getAnzlyzedDataString())

def pattern4400(data,count,debug=False): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isBigNegative():
        
        data[count + 5].set6RowsStatus(44)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern4400(data,count,debug=False): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isBigNegative():
        
        data[count + 4].set5RowsStatus(44)
        if debug:
            print(data[count + 4].get5RowsStatus().getAnzlyzedDataString())

def pattern4401(data,count,debug=False): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isBigNegative():
        
        data[count + 5].set6RowsStatus(44)
        if debug:
            print(data[count + 5].get6RowsStatus().getAnzlyzedDataString())

def pattern4402(data,count,debug=False): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isSmall()       and not existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 6].isBigNegative():
        
        data[count + 6].set7RowsStatus(44)
        if debug:
            print(data[count + 6].get7RowsStatus().getAnzlyzedDataString())

def pattern4403(data,count,debug=False): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isSmall()       and not existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 6].isSmall()       and not existsWindow(data[count + 5],data[count + 6]) and \
        data[count + 7].isBigNegative():
        
        data[count + 7].set8RowsStatus(44)
        if debug:
            print(data[count + 7].get8RowsStatus().getAnzlyzedDataString())
