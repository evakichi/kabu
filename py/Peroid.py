import Calender
import datetime

def getDates(fromDistance,toDistance) -> (str,str):
    current_datetime = datetime.datetime.today()

    fromDate = current_datetime + datetime.timedelta(days=-1*fromDistance)
    toDate = current_datetime + datetime.timedelta(days=-1*toDistance)

    return fromDate.strftime('%Y%M%d'),toDate.strftime('%Y%M%d')