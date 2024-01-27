import datetime
import requests
import json

class TradingCalender:
    
    date = None
    division = ['非営業日','営業日','東証半日立会日','非営業日(祝日取引あり)']


    def __init__(self,idToken) -> None:
        headers = {'Authorization': f'Bearer {idToken}'}
        self.HolidayDivision = requests.get(f'https://api.jquants.com/v1/markets/trading_calendar', headers=headers)
        self.HolidayDivisionJson = self.HolidayDivision.json()
        #print(self.HolidayDivisionJson)

    def isBusinessDay(self,date):
        for hd in self.HolidayDivisionJson['trading_calendar']:
            if hd['Date'] == date and (hd['HolidayDivision']=='1' or hd['HolidayDivision']=='2' or hd['HolidayDivision']=='3'):
                return True
        return False