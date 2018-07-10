import datetime, os

from peewee import *

preAccrual = {
    59: [100.928, "Wheeler"], 
    25: [169.232, "Ketrow"], 
    24: [148.008, "Gaylord_Greg"],
    39: [91.852, "Bernard"],
    65: [13.842, "Ballard"],
    37: [84.912, "McLaughlin"],
    66: [3.845, "Saxe"],
    47: [88.286, "Rounds"],
    23: [108.476, "Gaylord_Garan"],
    64: [5.383, "Williams"]}

db = SqliteDatabase('TimeOff.db')

class BaseModel(Model):
    class Meta:
        database = db

class Employee(BaseModel):
    employeeNumber = IntegerField(primary_key=True, unique=True)
    lastName = CharField(max_length=20)
    firstName = CharField(max_length=20)
    hireDate = DateField(null=False)
    password = CharField(max_length=20)

class Vacation(BaseModel):
    employeeNumber = IntegerField()
    vacationDate = DateField(null=False)
    hoursUsed = IntegerField(default=8)

class HolidayCalendar(BaseModel):
    holidayDate = DateField(primary_key=True, unique=True)
    description = TextField()

def initialize():
    db.connect()
    db.create_tables([Employee, Vacation, HolidayCalendar], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def dateToString(dateinput):
    return dateinput.strftime("%m/%d/%Y")

def stringToDate(datestring):
    dateSplit = datestring.split("/")
    if len(dateSplit[2]) == 4:
        return datetime.date(dateSplit[2], dateSplit[0], dateSplit[1])
    elif len(dateSplit[2]) == 2:
        dateSplit[2] = "20"+dateSplit[2]
        return datetime.date(int(dateSplit[2]), int(dateSplit[0]), int(dateSplit[1])) 

def cycleWeekday(dtinput):
    if dtinput.weekday() < 3:
        return dtinput + datetime.timedelta(days=1)
    else:
        return dtinput + datetime.timedelta(days=3)

def isHoliday(inputDate):
    try:
        HolidayCalendar.get(HolidayCalendar.holidayDate == inputDate)
        return True
    except:
        return False

def scheduleVacation():
    clear()
    print("Add Vacation Record")
    print("+"*50)
    empnum = int(input('Enter Employee Number > '))
    continueTrap = True
    while continueTrap is True:
        dateRequest = input('Enter Requested Vacation Date (MM/DD/YYYY)or exit > ')
        if dateRequest == 'exit':
            continueTrap = False
        else:
            dateRequest = stringToDate(dateRequest)
            hours = input('Enter 8 for full day, 4 for half day > ')
            Vacation.create(employeeNumber=empnum, vacationDate=dateRequest, hoursUsed=hours)
    
def accrualRate(runDate, hireDate):
    td = runDate - hireDate
    #accrual rate, in hours per day, after 5 years of service (3 weeks)
    if td.days > 1825:
        return .32876712
    #accrual rate, in hours per day, after 3 years of service (2 weeks)
    elif td.days > 1095:
        return .21917808
    #accrual rate, in hours per day, starting (1 week)
    else:
        return .10958904

def accrualCalc(empnum):
    preAccrualStart = datetime.date(2017, 2, 6)
    runningAccrual = 0
    #apply accrued time prior to accrual start date
    try:
        runningAccrual = preAccrual[empnum][0]
    except KeyError:
        pass
    query = Employee.get(Employee.employeeNumber == empnum)
    empName = "{} {}".format(query.firstName, query.lastName)
    hireDate  = query.hireDate
    maxAccrued = 0
    if hireDate > preAccrualStart:
        rt = hireDate
    else:
        rt = preAccrualStart
    while rt < datetime.date.today():
        rt += datetime.timedelta(days=1)
        dayPlus = accrualRate(rt, hireDate)
        #Check max allowable accrual
        if dayPlus == .10958904:
            maxAccrued = 80
        elif dayPlus == .21917808:
            maxAccrued = 160
        elif dayPlus == .32876712:
            maxAccrued = 240
        try:
            query = Vacation.get(Vacation.employeeNumber == empnum, Vacation.vacationDate == rt)
            if query.employeeNumber == empnum:
                dayMinus = query.hoursUsed
                #input("vacation used on {}".format(rt))
            else:
                dayMinus = 0
        except:
            dayMinus = 0
        if runningAccrual + dayPlus - dayMinus < maxAccrued:
            runningAccrual = runningAccrual + dayPlus - dayMinus
            #print("{} | {} + {} - {}".format(rt, runningAccrual, dayPlus, dayMinus))
        else:
            runningAccrual = maxAccrued
            #print(runningAccrual)
        accruedDays = round((runningAccrual/8),2)
    print ("{} | Total Vacation Available: {} Days".format(empName, accruedDays))

#start of App-------------------------------------------------------
if __name__ == "__main__":
    initialize()
    scheduleVacation()
    for employee in Employee.select():
        #print("{} {}".format(employee.firstName, employee.lastName))
        #cycle through employee numbers------------
        accrualCalc(employee.employeeNumber)
    #accrualCalc(39)
    db.close()