from datetime import datetime
import dateutil.parser

# A class for splitting the date from dateTime format into day, month and year.
class Finder: 

    def __init__(self, dateString):
        self.dateString = dateString
        self.dateTime = dateutil.parser.parse(dateString) 

    def findYear(self):
        year = self.dateTime.strftime('%Y')
        return year

    def findMonth(self):
        month = self.dateTime.strftime('%m')
        return month
    
    def findDay(self):
        day = self.dateTime.strftime('%d')
        return day

    