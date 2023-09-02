import os
import requests
import json
import openpyxl
import pathlib

mail = os.environ.get('J_QUANTS_MAIL_ADDRESS')
passwd = os.environ.get('J_QUANTS_PASSWD')

home = os.environ.get('HOME')

from_date = "20210610"
to_date = "20230610"

data={"mailaddress":mail, "password":passwd}
refreshToken_post = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
refreshToken_json = refreshToken_post.json()
refreshToken = refreshToken_json['refreshToken']
print(refreshToken)
idToken_post = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refreshToken}")
idToken_json = idToken_post.json()
idToken = idToken_json['idToken']
print(idToken)

headers = {'Authorization': 'Bearer {}'.format(idToken)}
information_get = requests.get(f"https://api.jquants.com/v1/listed/info", headers=headers)
information_json = information_get.json()

os.makedirs(os.path.join(home,"daily_quotes/"),exist_ok=True)
between = f"{from_date}-{to_date}"
path = os.path.join(home,"daily_quotes/",f"{from_date}-{to_date}.xlsx")
workbook = openpyxl.Workbook()
worksheet = workbook.get_sheet_by_name('Sheet')
workbook.remove(worksheet)
print(path)
for information in information_json['info']:
    code = information['Code']
    print(code)
    daily_quotes_get = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={code}&from={from_date}&to={to_date}", headers=headers)
    daily_quotes_json = daily_quotes_get.json()
    worksheet = workbook.create_sheet(title=code)
    worksheet['A1']="Date"
    worksheet['B1']="Open"
    worksheet['C1']="High"
    worksheet['D1']="Low"
    worksheet['E1']="Close"
    worksheet['F1']="UpperLimit"
    worksheet['G1']="LowerLimit"
    worksheet['H1']="Volume"
    worksheet['I1']="TurnoverValue"
    worksheet['J1']="AdjustmentFactor"
    worksheet['K1']="AdjustmentOpen"
    worksheet['L1']="AdjustmentHigh"
    worksheet['M1']="AdjustmentLow"
    worksheet['N1']="AdjustmentClose"
    worksheet['O1']="AdjustmentVolume"

    count = 2
    for daily_quote in daily_quotes_json['daily_quotes']:
        Date = daily_quote['Date']
        worksheet[f"A{count}"]=Date

        Open = daily_quote['Open']
        worksheet[f"B{count}"]=Open

        High = daily_quote['High']
        worksheet[f"C{count}"]=High

        Low = daily_quote['Low']
        worksheet[f"D{count}"]=Low

        Close = daily_quote['Close']
        worksheet[f"E{count}"]=Close

        UpperLimit = daily_quote['UpperLimit']
        worksheet[f"F{count}"]=UpperLimit

        LowerLimit = daily_quote['LowerLimit']
        worksheet[f"G{count}"]=LowerLimit

        Volume = daily_quote['Volume']
        worksheet[f"H{count}"]=Volume

        TurnoverValue = daily_quote['TurnoverValue']
        worksheet[f"I{count}"]=TurnoverValue

        AdjustmentFactor = daily_quote['AdjustmentFactor']
        worksheet[f"J{count}"]=AdjustmentFactor

        AdjustmentOpen = daily_quote['AdjustmentOpen']
        worksheet[f"K{count}"]=AdjustmentOpen

        AdjustmentHigh = daily_quote['AdjustmentHigh']
        worksheet[f"L{count}"]=AdjustmentHigh

        AdjustmentLow = daily_quote['AdjustmentLow']
        worksheet[f"M{count}"]=AdjustmentLow

        AdjustmentClose = daily_quote['AdjustmentClose']
        worksheet[f"N{count}"]=AdjustmentClose

        AdjustmentVolume = daily_quote['AdjustmentVolume']
        worksheet[f"O{count}"]=AdjustmentVolume

        count += 1
workbook.save(path)
workbook.close()