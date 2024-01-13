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

def pattern00(data,count): #三空叩き込み
    if  data[count    ].isNegative() and isDesc(data[count    ],data[count + 1]) and \
        existsWindow(data[count    ],data[count +1]) and \
        data[count + 1].isNegative() and isDesc(data[count + 1],data[count + 2]) and \
        existsWindow(data[count + 1],data[count +2]) and \
        data[count + 2].isNegative() and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count +3]) and \
        data[count + 3].isNegative() and isDesc(data[count + 3],data[count + 4]):

        data[count + 4].set5DaysStatus(0)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern01(data,count): #三手大陰線
    if  data[count    ].isNegative()    and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isBigNegative() and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isBigNegative() and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isBigNegative() and isDesc(data[count + 3],data[count + 4]):

        data[count + 4].set5DaysStatus(1)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern02(data,count): #最後の抱き陰線
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallPositive() and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigNegative():

        data[count + 4].set5DaysStatus(2)
        print(data[count + 4].get5DaysStatus().getAnzlyzedDataString())

def pattern03(data,count): #明けの明星
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
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

def pattern04(data,count): #捨て子底
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 3].isCross()         and isAsce(data[count + 3],data[count + 4]) and \
        existsWindow(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(4)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern05(data,count): #大陰線のはらみ寄せ
    avg = (data[count + 2].getOpen()+data[count +2].getClose())/2
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isCross()         and isAsce(data[count + 3],data[count + 4]) and \
        avg * 0.9 < data[count + 3].getOpen() < avg *1.1 and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(5)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern06(data,count): #たくり線
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isBigNegative()   and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 3].getLow() < data[count + 3].getClose() and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(6)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern07(data,count): #勢力線
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 3].getLow() < data[count + 3].getOpen() and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(7)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern08(data,count): #陰の陰はらみ
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isBigNegative()   and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallNegative() and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 2].getClose() < data[count + 3].getClose() and \
        data[count + 2].getOpen() > data[count + 3].getOpen() and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(8)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern09(data,count): #放れ五手黒一本底
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        existsWindow(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]):

        data[count + 6].set7DaysStatus(9)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern10(data,count): #やぐら底
    if  data[count    ].isBigNegative()   and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isPositive()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and \
        data[count + 3].isPositive()      and \
        data[count + 4].isNegative()      and \
        data[count + 5].isBigPositive()   and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(10)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern11(data,count): #小幅上放れ黒線
    if  data[count    ].isNegative()      and isFlat(data[count    ],data[count + 1]) and \
        data[count + 1].isPositive()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isFlat(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isNegative()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(11)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern12(data,count): #放れ七手の変化底
    if  data[count    ].isBigNegative()   and isDesc(data[count    ],data[count + 1]) and \
        existsWindow(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isFlat(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive():

        data[count + 5].set6DaysStatus(12)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern13(data,count): #連続下げ放れ三つ星
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        existsWindow(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isFlat(data[count + 3],data[count + 4]) and \
        data[count + 4].isCross()         and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isBigPositive():

        data[count + 5].set6DaysStatus(13)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern14(data,count): #逆襲線
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        existsWindow(data[count + 2],data[count + 3]) and \
        data[count + 2].isBigPositive()   and isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(14)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern15(data,count): #抱き陽線
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(16)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern16(data,count): #寄り切り陽線
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isNegative()      and isDesc(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and data[count + 2].getClose() == data[count + 3].getOpen() and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isBigPositive()   and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(16)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern17(data,count): #赤三兵
    if  data[count    ].isSmallNegative() and \
        data[count + 1].isSmallNegative() and \
        data[count + 2].isSmallNegative() and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isSmallPositive() and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isSmallPositive() and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isSmallPositive() and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(17)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern18(data,count): #下位の陽線五本
    if  data[count    ].isNegative()      and isDesc(data[count    ],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isPositive()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(18)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern19(data,count): #押え込み線
    if  data[count    ].isPositive()      and isAsce(data[count    ],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive()      and isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(19)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern20(data,count): #上げの差し込み線
    if  data[count    ].isPositive()      and isAsce(data[count    ],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isAsce(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]) and \
        isAsce(data[count + 5],data[count + 6]):

        data[count + 6].set7DaysStatus(20)
        print(data[count + 6].get7DaysStatus().getAnzlyzedDataString())

def pattern21(data,count): #上げ三法
    if  data[count    ].isPositive()      and isAsce(data[count    ],data[count + 1]) and \
        data[count + 1].isBigPositive()   and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isDesc(data[count + 3],data[count + 4]) and \
        data[count + 4].isNegative()      and isAsce(data[count + 4],data[count + 5]) and \
        data[count + 5].isPositive():

        data[count + 5].set6DaysStatus(21)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern22(data,count): #カブセの上抜け
    if  data[count    ].isPositive()      and isAsce(data[count    ],data[count + 1]) and \
        data[count + 1].isPositive()      and \
        data[count + 2].isNegative()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        data[count + 4].isPositive()      and isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(22)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())

def pattern23(data,count): #カブセの上抜け
    if  data[count    ].isPositive()      and isAsce(data[count    ],data[count + 1]) and \
        data[count + 1].isPositive()      and isAsce(data[count + 1],data[count + 2]) and \
        data[count + 2].isPositive()      and isDesc(data[count + 2],data[count + 3]) and \
        data[count + 3].isNegative()      and isAsce(data[count + 3],data[count + 4]) and \
        isAsce(data[count + 4],data[count + 5]):

        data[count + 5].set6DaysStatus(23)
        print(data[count + 5].get6DaysStatus().getAnzlyzedDataString())
