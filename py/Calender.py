import datetime
import requests
import json

class Calender:
    
    date = None
    
    def __init__(self,fromDate,toDate,headers) -> None:
        self.date = list()
        data = requests.get(f'https://api.jquants.com/v1/markets/trading_calendar?holidaydivision=1&from={fromDate}&to={toDate}', headers=headers)
        d = data.json()
        print(d)
        pass