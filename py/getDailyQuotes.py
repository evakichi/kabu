import CommonPackage
import Period
import Token
import Brand

import os
import requests
import openpyxl
import math
from multiprocessing import Process,Queue
import Data
import TradingCalender

def loadAndCalc(brandData,fromDate,toDate,headers,count,queue,debug):
    print(f'{count}:{brandData.getDate()}:{brandData.getCode()}:{brandData.getCompanyName()}({brandData.getCompanyNameEnglish()}):',end="")
    print(f'{brandData.getSector17CodeName()}({brandData.getSector17Code()}):{brandData.getSector33CodeName()}({brandData.getSector33Code()}):',end="")
    print(f'{brandData.getScaleCategory()}:{brandData.getMarketCodeName()}({brandData.getMarketCode()}):')
    
    daily_quotes_get = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={brandData.getCode()}&from={fromDate}&to={toDate}", headers=headers)
    daily_quotes_json = daily_quotes_get.json()

    datasheet = list()
    for daily_quote in daily_quotes_json['daily_quotes']:
        data = Data.Data(daily_quote,0.05,0.05)
        if not data.isNone():
            datasheet.append(data)

    previous = None
    for data in datasheet:
        if not previous == None:
            data.setFactor(previous)
        previous = data

    length = len(datasheet)
    for counter,data in enumerate(datasheet):
        if counter + 8 >= length:
            continue
        CommonPackage.pattern083200(datasheet,counter,debug)#新値八手利食い線
        CommonPackage.pattern083303(datasheet,counter,debug)#三手放れ寄せ線
        CommonPackage.pattern084100(datasheet,counter,debug)#抱き陽線
        CommonPackage.pattern084200(datasheet,counter,debug)#つたい線の打ち返し
        CommonPackage.pattern084300(datasheet,counter,debug)#放れ五手赤一本
        CommonPackage.pattern084400(datasheet,counter,debug)#放れ七手大黒
        if counter + 7 >= length:
            continue
        CommonPackage.pattern070900(datasheet,counter,debug)#放れ五手黒一本底
        CommonPackage.pattern071000(datasheet,counter,debug)#やぐら底
        CommonPackage.pattern071100(datasheet,counter,debug)#小幅上放れ黒線
        CommonPackage.pattern071700(datasheet,counter,debug)#赤三兵
        CommonPackage.pattern071800(datasheet,counter,debug)#下位の陽線五本
        CommonPackage.pattern071900(datasheet,counter,debug)#押え込み線
        CommonPackage.pattern072000(datasheet,counter,debug)#上げの差し込み線
        CommonPackage.pattern072700(datasheet,counter,debug)#並び赤
        CommonPackage.pattern072800(datasheet,counter,debug)#上放れ陰線二本連続
        CommonPackage.pattern072900(datasheet,counter,debug)#上位の連続大陽線
        CommonPackage.pattern073302(datasheet,counter,debug)#三手放れ寄せ線
        CommonPackage.pattern074600(datasheet,counter,debug)#下放れ三手
        CommonPackage.pattern074700(datasheet,counter,debug)#下げ三法
        CommonPackage.pattern074800(datasheet,counter,debug)#三手打ち
        if counter + 6 >= length:
            continue
        CommonPackage.pattern060300(datasheet,counter,debug)#明けの明星
        CommonPackage.pattern060400(datasheet,counter,debug)#捨て子底
        CommonPackage.pattern060500(datasheet,counter,debug)#大陰線のはらみ寄せ
        CommonPackage.pattern060600(datasheet,counter,debug)#たくり線
        CommonPackage.pattern060700(datasheet,counter,debug)#勢力線
        CommonPackage.pattern060800(datasheet,counter,debug)#陰の陰はらみ
        CommonPackage.pattern061200(datasheet,counter,debug)#放れ七手の変化底
        CommonPackage.pattern061300(datasheet,counter,debug)#連続下げ放れ三つ星
        CommonPackage.pattern061400(datasheet,counter,debug)#逆襲線
        CommonPackage.pattern061500(datasheet,counter,debug)#抱き陽線
        CommonPackage.pattern061600(datasheet,counter,debug)#寄り切り陽線
        CommonPackage.pattern062100(datasheet,counter,debug)#上げ三法
        CommonPackage.pattern062200(datasheet,counter,debug)#カブセの上抜け
        CommonPackage.pattern062300(datasheet,counter,debug)#上伸途上の連続タスキ
        CommonPackage.pattern062400(datasheet,counter,debug)#上放れタスキ
        CommonPackage.pattern062500(datasheet,counter,debug)#上伸途上のクロス
        CommonPackage.pattern062600(datasheet,counter,debug)#上げの三つ星
        CommonPackage.pattern063000(datasheet,counter,debug)#波高い線
        CommonPackage.pattern063301(datasheet,counter,debug)#三手放れ寄せ線
        CommonPackage.pattern063400(datasheet,counter,debug)#行き詰まり線
        CommonPackage.pattern063500(datasheet,counter,debug)#三羽ガラス
        CommonPackage.pattern063600(datasheet,counter,debug)#首吊り線
        CommonPackage.pattern063700(datasheet,counter,debug)#上位の上放れ陰線
        CommonPackage.pattern063800(datasheet,counter,debug)#宵の明星
        CommonPackage.pattern063900(datasheet,counter,debug)#陽の陽はらみ
        CommonPackage.pattern064000(datasheet,counter,debug)#最後の抱き陽線
        CommonPackage.pattern065000(datasheet,counter,debug)#化け線
        CommonPackage.pattern065100(datasheet,counter,debug)#下げ足のクロス
        CommonPackage.pattern065200(datasheet,counter,debug)#下放れ黒二本
        CommonPackage.pattern065300(datasheet,counter,debug)#下げの三つ星
        CommonPackage.pattern065400(datasheet,counter,debug)#上位の陰線五本
        CommonPackage.pattern065500(datasheet,counter,debug)#寄り切り陰線    

        if counter + 5 >= length:
            continue
        CommonPackage.pattern050000(datasheet,counter,debug)#三空叩き込み
        CommonPackage.pattern050100(datasheet,counter,debug)#三手大陰線
        CommonPackage.pattern050200(datasheet,counter,debug)#最後の抱き陰線
        CommonPackage.pattern053100(datasheet,counter,debug)#三空踏み上げ
        CommonPackage.pattern053300(datasheet,counter,debug)#三手放れ寄せ線
        CommonPackage.pattern054500(datasheet,counter,debug)#差し込み線
        CommonPackage.pattern054900(datasheet,counter,debug)#下落途上の連続タスキ
    queue.put((brandData,datasheet))

if __name__ == '__main__':
    numOfThreads = 20

    homeDir = os.environ.get('HOME')
    refreshToken, idToken = Token.getTokens()
    for d in range(Period.fiveYears):
        fromDate,toDate = Period.getDates(d+1,d+1)
    path = CommonPackage.createDir(os.path.join(homeDir,CommonPackage.dataDir))
    period = f"{fromDate}-{toDate}"

    brandData = [Brand.BrandData(info) for info in Brand.BrandData.getBrandInfo(idToken)]
    headers = {'Authorization': f'Bearer {idToken}'}

    cal = TradingCalender.Calender(fromDate,toDate,headers)


    xlsxPath = os.path.join(homeDir,"daily_quotes/",period+".xlsx")

    workbook = openpyxl.Workbook()
    worksheet = workbook.get_sheet_by_name('Sheet')
    workbook.remove(worksheet)
    print(xlsxPath)



    datasheets = list()
    length = len(brandData)
    for iter in range(math.ceil(length/numOfThreads)):
        process = list()
        queue = list()
        nextIter = CommonPackage.getNextInterIter(length,iter,numOfThreads)
        for thread in range(nextIter):
            queue.append(Queue())
        for thread in range(nextIter):
            process.append(Process(target=loadAndCalc,args=(brandData[iter*numOfThreads+thread],fromDate,toDate,headers,iter*numOfThreads+thread,queue[thread],False)))
        for thread in range(nextIter):
            process[thread].start()
        for q in queue:
            datasheets.append(q.get())
        for thread in range(nextIter):
            process[thread].join()
    for data in datasheets:
        brandData,sheets = data
        worksheet = workbook.create_sheet(title=brandData.getCode())
        for count, d in enumerate(sheets,start=3):
            if count == 3:
                worksheet['A1']=brandData.getDate()
                worksheet['B1']=brandData.getCode()
                worksheet['C1']=brandData.getCompanyName()
                worksheet['D1']=brandData.getCompanyNameEnglish()
                worksheet['E1']=brandData.getSector17Code()
                worksheet['F1']=brandData.getSector17CodeName()
                worksheet['G1']=brandData.getSector33Code()
                worksheet['H1']=brandData.getSector33CodeName()
                worksheet['I1']=brandData.getScaleCategory()
                worksheet['J1']=brandData.getMarketCode()
                worksheet['K1']=brandData.getMarketCodeName()
                cellData = d.getCellString().getCellData()
                for a,c in enumerate(cellData):
                    worksheet[f'{c[0]}2'] = c[1]
            d.write(worksheet,count)

    workbook.save(xlsxPath)
    workbook.close()