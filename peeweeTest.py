import datetime, os

from peewee import *

sqlite_db = SqliteDatabase(':memory:')

class BaseModel(Model):
	class Meta:
		database = sqlite_db

class HolidayCalendar(BaseModel):
	holidayDate = DateTimeField()
	description = TextField()

def initialize():
    sqlite_db.connect()
    sqlite_db.create_tables([HolidayCalendar], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def dateConvert(datestring):
	try:
	    dateFormatted = datetime.datetime.strptime(datestring, "%m/%d/%Y")
	    return dateFormatted
	except ValueError:
	    print("Error: Incorrect date Format.")


def addHoliday():
	holidate = input("Enter Date of Holiday --MM/DD/YYYY-- >> ")
	hrdtF = dateConvert(holidate)
	holDesc = input('Enter Holiday Description >> ')
	HolidayCalendar.create(holidayDate=hrdtF, description=holDesc)

def viewCalendar():
	for holiday in HolidayCalendar.select():
		displayDate = holiday.holidayDate
		description = holiday.description
		print("{} | {}".format(displayDate.strftime("%m/%d/%Y"), description))
	input("\n\n\nPress Enter When Finished")
		
def isHoliday(inputDate):
	query = HolidayCalendar.select(HolidayCalendar.holidayDate)
	inputDateString = inputDate.strftime("%m/%d/%Y")
	answer = False
	for x in query:
		print(x())
		input()
		querystring = x.strftime("%m/%d/%Y")
		if inputDateString == querystring:        
			answer = True
		else:
			pass
	return answer
    

initialize()

while True:
	
	menu = int(input("Enter 1 to add Holiday\nEnter 2 to View Current Holiday Calendar\nEnter 3 to Exit >> "))
	if menu == 1:
		clear()
		addHoliday()
	elif menu == 2:
		clear()
		viewCalendar()

	elif menu == 3:
		sqlite_db.close()
		exit()
	elif menu == 4:
		answer = isHoliday(datetime.datetime.now())
		print(answer)
	else:
		print("Invalid Entry")