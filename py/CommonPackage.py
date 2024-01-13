import requests
import os
import json
import datetime
import Data
import numpy as np

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

def pattern0000(data,count): #三空叩き込み
    if  data[count + 0].isNegative() and isDesc(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count +1]) and \
        data[count + 1].isNegative() and isDesc(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count +2]) and \
        data[count + 2].isNegative() and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count +3]) and \
        data[count + 3].isNegative() and isDesc(data[count + 3],data[count + 4]):

        data[count + 4].set5DaysStatus(0)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern0100(data,count): #三手大陰線
    if  data[count + 0].isNegative()    and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigNegative() and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isBigNegative() and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isBigNegative() and isDesc(data[count + 3],data[count + 4]):

        data[count + 4].set5DaysStatus(1)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern0200(data,count): #最後の抱き陰線
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallPositive() and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigNegative():

        data[count + 4].set5DaysStatus(2)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern0300(data,count): #明けの明星
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]) and \
        data[count + 6].isPositive():

        data[count + 6].set7DaysStatus(3)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern0400(data,count): #捨て子底
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isCross()         and isAsce(data[count + 3],data[count + 4]) and \
        existsWindow(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(4)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern0500(data,count): #大陰線のはらみ寄せ
    avg = (data[count + 2].getOpen()+data[count +2].getClose())/2
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isCross()         and isAsce(data[count + 3],data[count + 4]) and \
        avg * 0.9 < data[count + 3].getOpen() < avg *1.1 and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(5)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern0600(data,count): #たくり線
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isBigNegative()   and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 3].getLow() < data[count + 3].getClose() and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(6)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern0700(data,count): #勢力線
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 3].getLow() < data[count + 3].getOpen() and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(7)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern0800(data,count): #陰の陰はらみ
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isBigNegative()   and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallNegative() and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 2].getClose() < data[count + 3].getClose() and \
        data[count + 2].getOpen() > data[count + 3].getOpen() and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(8)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern0900(data,count): #放れ五手黒一本底
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]):

        data[count + 6].set7DaysStatus(9)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern1000(data,count): #やぐら底
    if  data[count + 0].isBigNegative()   and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and \
        data[count + 3].isPositive()      and \
        data[count + 4].isNegative()      and \
        data[count + 5].isBigPositive()   and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(10)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern1100(data,count): #小幅上放れ黒線
    if  data[count + 0].isNegative()      and isFlat(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isFlat(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(11)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern1200(data,count): #放れ七手の変化底
    if  data[count + 0].isBigNegative()   and isDesc(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isFlat(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive():

        data[count + 5].set6DaysStatus(12)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern1300(data,count): #連続下げ放れ三つ星
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isFlat(data[count + 3],data[count + 4]) and \
        data[count + 4].isCross()         and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isBigPositive():

        data[count + 5].set6DaysStatus(13)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern1400(data,count): #逆襲線
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 2].isBigPositive()   and isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(14)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern1500(data,count): #抱き陽線
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(16)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern1600(data,count): #寄り切り陽線
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and data[count + 2].getClose() == data[count + 3].getOpen() and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(16)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern1700(data,count): #赤三兵
    if  data[count + 0].isSmallNegative() and \
        data[count + 1].isSmallNegative() and \
        data[count + 2].isSmallNegative() and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallPositive() and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isSmallPositive() and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isSmallPositive() and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(17)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern1800(data,count): #下位の陽線五本
    if  data[count + 0].isNegative()      and isDesc(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(18)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern1900(data,count): #押え込み線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(19)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern2000(data,count): #上げの差し込み線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(20)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern2100(data,count): #上げ三法
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive()   and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive():

        data[count + 5].set6DaysStatus(21)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern2200(data,count): #カブセの上抜け
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(22)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern2300(data,count): #上伸途上の連続タスキ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(23)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern2400(data,count): #上放れタスキ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(24)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern2500(data,count): #上伸途上のクロス
    if  data[count + 0].isPositive()      and \
        data[count + 1].isPositive()      and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isBigPositive()   and \
        data[count + 4].isCross()         and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(25)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern2600(data,count): #上げの三つ星
    if  data[count + 0].isPositive()      and \
        data[count + 1].isPositive()      and \
        data[count + 2].isSmallNegative() and \
        data[count + 3].isSmallPositive() and \
        data[count + 4].isSmallNegative() and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(26)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern2700(data,count): #並び赤
    if  data[count + 0].isPositive()      and \
        data[count + 1].isPositive()      and \
        data[count + 2].isPositive()      and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallPositive() and \
        data[count + 4].isSmallPositive() and isAsce(data[count + 4],data[count + 5]) and \
        isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(27)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern2800(data,count): #上放れ陰線二本連続
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative()      and isDesc(data[count + 5],data[count + 6]) :

        data[count + 6].set7DaysStatus(28)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern2900(data,count): #上位の連続大陽線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isAsce(data[count + 4],data[count + 5]) and \
        existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 5].isBigPositive()   and isAsce(data[count + 5],data[count + 6]) and \
        data[count + 6].isBigPositive():

        data[count + 6].set7DaysStatus(29)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern3000(data,count): #波高い線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 3].getClose()*1.10 < data[count + 4].getHigh() and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]):
        
        data[count + 5].set6DaysStatus(30)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern3100(data,count): #三空踏み上げ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]):
        
        data[count + 4].set5DaysStatus(31)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern3200(data,count): #新値八手利食い線
    if  data[count + 0].max() < data[count + 1].max() < data[count + 2].max() < data[count + 3].max() < \
        data[count + 4].max() < data[count + 4].max() < data[count + 6].max() < data[count + 7].max():
        
        data[count + 7].set8DaysStatus(32)
        print(data[count + 7].get8DaysStatus().getAnzlyzedDataString())

def pattern3300(data,count): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 4].isCross():
        
        data[count + 4].set5DaysStatus(33)
        print(data[count + 5].get5DaysStatus().getAnzlyzedDataString())

def pattern3301(data,count): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isCross():
        
        data[count + 5].set6DaysStatus(33)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern3302(data,count): #三手放れ寄せ線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]) and \
        data[count + 6].isCross():
        
        data[count + 6].set7DaysStatus(33)
        print(data[count + 5].get7DaysStatus().getAnzlyzedDataString())

def pattern3400(data,count): #行き詰まり線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        existsWindow(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isBigPositive()   and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 3].getHigh() > data[count].getClose()*1.10:
        
        data[count + 5].set6DaysStatus(34)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern3500(data,count): #三羽ガラス
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative() and \
        data[count + 3].getClose() < data[count + 4].getOpen() and \
        data[count + 4].getClose() < data[count + 5].getOpen():
        
        data[count + 5].set6DaysStatus(35)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern3600(data,count): #首吊り線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].getLow() < data[count + 3].getOpen()*0.90 and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]) and \
        isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6DaysStatus(36)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern3700(data,count): #上位の上放れ陰線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6DaysStatus(37)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern3800(data,count): #宵の明星
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]) and \
        existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6DaysStatus(38)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern3900(data,count): #陽の陽はらみ
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 3].getClose()  > data[count + 4].getClose() and \
        data[count + 3].getOpen() < data[count + 4].getOpen() and \
        isDesc(data[count + 4],data[count + 5]):
        
        data[count + 5].set6DaysStatus(39)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern4000(data,count): #最後の抱き陽線
    if  data[count + 0].isPositive()      and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 3].getOpen()  < data[count + 4].getClose() and \
        data[count + 3].getClose() > data[count + 4].getOpen():
        
        data[count + 5].set6DaysStatus(40)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern4100(data,count): #抱き陽線
    if  isAsce(data[count + 0],data[count + 1]) and \
        isAsce(data[count + 1],data[count + 2]) and \
        isAsce(data[count + 2],data[count + 3]) and \
        isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]) and \
        data[count + 4].isBigNegative() and isDesc(data[count + 5],data[count + 6]) and \
        isDesc(data[count + 6],data[count + 7]) and \
        data[count + 4].getOpen()  > data[count + 5].getClose() and \
        data[count + 4].getClose() < data[count + 5].getOpen():
        
        data[count + 7].set8DaysStatus(41)
        print(data[count + 7].get8DaysStatus().getAnzlyzedDataString())

def pattern4200(data,count): #つたい線の打ち返し
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()    and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()    and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()    and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()    and isDesc(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative()    and isAsce(data[count + 5],data[count + 6]) and \
        data[count + 6].isBigPositive() and isDesc(data[count + 6],data[count + 7]):
        
        data[count + 7].set8DaysStatus(42)
        print(data[count + 7].get8DaysStatus().getAnzlyzedDataString())

def pattern4300(data,count): #放れ五手赤一本
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isPositive()    and isAsce(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()    and \
        data[count + 3].isNegative()    and \
        data[count + 4].isPositive()    and \
        data[count + 5].isNegative()    and \
        data[count + 6].isBigPositive() and isDesc(data[count + 6],data[count + 7]):
        
        data[count + 7].set8DaysStatus(43)
        print(data[count + 7].get8DaysStatus().getAnzlyzedDataString())

def pattern4400(data,count): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isBigNegative():
        
        data[count + 5].set6DaysStatus(44)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern4400(data,count): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isBigNegative():
        
        data[count + 4].set5DaysStatus(44)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern4401(data,count): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isBigNegative():
        
        data[count + 5].set6DaysStatus(44)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern4402(data,count): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isSmall()       and not existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 6].isBigNegative():
        
        data[count + 6].set7DaysStatus(44)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern4403(data,count): #放れ七手大黒
    if  data[count + 0].isPositive()    and isAsce(data[count + 0],data[count + 1]) and \
        data[count + 1].isBigPositive() and \
        data[count + 2].isSmall()       and not existsWindow(data[count + 1],data[count + 2]) and \
        data[count + 3].isSmall()       and not existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 4].isSmall()       and not existsWindow(data[count + 3],data[count + 4]) and \
        data[count + 5].isSmall()       and not existsWindow(data[count + 4],data[count + 5]) and \
        data[count + 6].isSmall()       and not existsWindow(data[count + 5],data[count + 6]) and \
        data[count + 7].isBigNegative():
        
        data[count + 7].set8DaysStatus(44)
        print(data[count + 7].get8DaysStatus().getAnzlyzedDataString())
