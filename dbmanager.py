#!python3
#dbmanager.py - program for manipulating sqlite database

import datetime, os

from peewee import *

preAccrual = {
    32: [76.39, "Doland"], 
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

db = SqliteDatabase('Employees.db')

class BaseModel(Model):
    class Meta:
        database = db

class Employee(BaseModel):
    employeeNumber = IntegerField(primary_key=True,max_length=4, unique=True)
    lastName = Charfield(max_length = 20)
    firstName = Charfield(max_length = 20)
    hireDate = Datefield(null=False)
    password = Charfield(max_length = 20)

class Vacation(BaseModel):
    employeeNumber = IntegerField(primary_key=True,max_length=4, unique=True)
    vacationDate = Datefield(null=False)
    hoursUsed = IntegerField(max_length=1, default=8)

class HolidayCalendar(BaseModel):
    holidayDate = DateTimeField()
    description = TextField()

def initialize():
    db.connect()
    db.create_tables([Employee, Vacation, HolidayCalendar], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def addEmployee():
     clear()
    print("Add A New Employee")
    print("+"*50)
    empnum = int(input("Enter Employee Number > "))
    lstnm = input("Enter Employee Last Name > ")
    fstnm = input("Enter Employee First Name > ")
    hrdt = input("Enter Date of Hire --MM/DD/YYYY-- > ")
    hrdtF = dateConvert(hrdt)
    pwd = input("Enter User Password > ")
    pwd2 = input("Re-enter Password > ")
    while pwd != pwd2:
        print("Password Mismatch...try again")
        pwd = input("Enter User Password > ")
        pwd2 = input("Re-enter Password > ")
    preAcc = input("Enter Accrued Vacation as of 2/6/2017")    
    clear()
    print('Adding Employee to Database...')
    Employee.create(employeeNumber=empnum, lastName=lstnm, firstName=fstnm, hireDate=hrdtF, password=pwd)
    time.sleep(1)
    print('Employee Successfully Added')
    time.sleep(1)
    clear()

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


def scheduleVacation():
    clear()
    print("Add Vacation Record")
    print("+"*50)
    empnum = int(input('Enter Employee Number > '))
    numdays = float(input('Enter Total Days Requested > '))
    if numdays > 1:
        strtdte = input('Enter Start Date --MM/DD/YYYY-- > ')
        strtdteF = dateConvert(strtdte)
        countdwn = numdays
        Vacation.create(employeeNumber=empnum, vacationDate=strtdteF, hoursUsed=8)
        while countdwn:
            countdwn -= 1
            if strtdteF.weekday() < 3:
                strtdteF += datetime.timedelta(days=1)
            else:
                strtdteF += datetime.timedelta(days=3)
            Vacation.create(employeeNumber=empnum, vacationDate=strtdteF, hoursUsed=8)            
    else:
        strtdte = input("Enter Requested Vacation Date > ")
        strtdteF = dateConvert(strtdte)
        if numdays == 1:
            Vacation.create(employeeNumber=empnum, vacationDate=strtdteF, hoursUsed=8)
        else:
            Vacation.create(employeeNumber=empnum, vacationDate=strtdteF, hoursUsed=4)

def accrualRate(hireDate):
    today = datetime.datetime.now()
    td = today - hireDate
    #accrual rate, in hours per day, after 5 years of service (3 weeks)
    if td.days > 1825:
        return .32876712
    #accrual rate, in hours per day, after 3 years of service (2 weeks)
    elif td.days > 1095:
        return .21917808
    #accrual rate, in hours per day, starting (1 week)
    else
        return .10958904

def accrualCalc(empnum):
    accrualStart = datetime.datetime(2017, 2, 6)


