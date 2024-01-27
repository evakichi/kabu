import TradingCalender
import datetime

fiveYears = 1825

class Period:

    def __init__ (self,fromDistance,toDistance)-> None:
        current_datetime = datetime.datetime.today()

        self.fromDate = current_datetime + datetime.timedelta(days=-1*fromDistance)
        self.toDate = current_datetime + datetime.timedelta(days=-1*toDistance)

    def getDate(distance):
        current_datetime = datetime.datetime.today()
        return current_datetime + datetime.timedelta(days=-1*distance)

    def getFromDate(self):
        return self.fromDate
    
    def getToDate(self):
        return self.toDate