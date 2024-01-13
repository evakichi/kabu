import requests
import os
import json
import datetime
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
 
def max(openVal,highVal,lowVal,closeVal):
    if openVal != None and closeVal != None:
        if openVal < closeVal:
            return closeVal
        else:
            return openVal
    else:
        return None

def min(openVal,highVal,lowVal,closeVal):
    if openVal != None and closeVal != None:
        if openVal > closeVal:
            return closeVal
        else:
            return openVal
    else:
        return None

def getAvg(openVal,highVal,lowVal,closeVal):
    return (openVal + highVal + lowVal + closeVal) / 4

def getRatio(openVal,highVal,lowVal,closeVal):
    return (closeVal - openVal) / getAvg(openVal,highVal,lowVal,closeVal)

def getAbsRatio(openVal,highVal,lowVal,closeVal):
    return abs(getRatio(openVal,highVal,lowVal,closeVal))

def isPositive(openVal,highVal,lowVal,closeVal):
    if not isNone(openVal,highVal,lowVal,closeVal) and openVal < closeVal:
        return True
    return False

def isNegative(openVal,highVal,lowVal,closeVal):
    if not isNone(openVal,highVal,lowVal,closeVal) and openVal > closeVal:
        return True
    return False

def isCross(openVal,highVal,lowVal,closeVal):
    if not isNone(openVal,highVal,lowVal,closeVal) and openVal == closeVal:
        return True
    return False

def isSmallPosoitive(openVal,highVal,lowVal,closeVal):
    if isPositive(openVal,highVal,lowVal,closeVal):
        if getAbsRatio(openVal,highVal,lowVal,closeVal) < 0.03:
            return True
    return False

def isBigPosoitive(openVal,highVal,lowVal,closeVal):
    if isPositive(openVal,highVal,lowVal,closeVal):
        if getAbsRatio(openVal,highVal,lowVal,closeVal) >= 0.03:
            return True
    return False

def isSmallNegative(openVal,highVal,lowVal,closeVal):
    if isNegative(openVal,highVal,lowVal,closeVal):
        if getAbsRatio(openVal,highVal,lowVal,closeVal) < 0.1:
            return True
    return False

def isBigNegative(openVal,highVal,lowVal,closeVal):
    if isNegative(openVal,highVal,lowVal,closeVal):
        if getAbsRatio(openVal,highVal,lowVal,closeVal) >= 0.1:
            return True
    return False

def getPastDays(worksheet,current,days):
    pastDaysOpen = list()
    pastDaysHigh = list()
    pastDaysLow = list()
    pastDaysClose = list()
    pastDaysRatio = list()
    pastDaysAbsRatio = list()
    
    for d in range(days,-1,-1):
        if not worksheet[f'B{current - d}'].value == None:
            pastDaysOpen.append(float(worksheet[f'B{current - d}'].value))
        else:
            pastDaysOpen.append(None)
        if not worksheet[f'C{current - d}'].value == None:
            pastDaysHigh.append(float(worksheet[f'E{current - d}'].value))
        else:
            pastDaysHigh.append(None)
        if not worksheet[f'D{current - d}'].value == None:
            pastDaysLow.append(float(worksheet[f'E{current - d}'].value))
        else:
            pastDaysLow.append(None)
        if not worksheet[f'E{current - d}'].value == None:
            pastDaysClose.append(float(worksheet[f'E{current - d}'].value))
        else:
            pastDaysClose.append(None)
            
        if pastDaysOpen[-1] != None and pastDaysHigh[-1] != None and pastDaysLow[-1] != None and pastDaysClose[-1] != None:
            pastDaysRatio.append(float(worksheet[f'Q{current - d}'].value))
            pastDaysAbsRatio.append(abs(float(worksheet[f'Q{current - d}'].value)))
        else:
            pastDaysRatio.append(-1.0)
            pastDaysAbsRatio.append(-1.0)
    return pastDaysOpen,pastDaysHigh,pastDaysLow,pastDaysClose,pastDaysRatio,pastDaysAbsRatio
