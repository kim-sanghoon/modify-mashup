from dateutil.parser import parse
from ..Time import *

def parseDate(isoString):
    monthStr = [
        'None', 'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August', 'September', 
        'October', 'November', 'December'
    ]
    date = parse(isoString)

    return {
        'month': monthStr[date.month],
        'day': str(date.day)
    }

def parseTime(isoString):
    time = parse(isoString)

    return Time(time.hour)