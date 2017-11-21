#!python3
#dbmanager.py - program for manipulating sqlite database

import datetime, os, re 

from peewee import *

db = SqliteDatabase('Employees')

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

def initialize():
    db.connect()
    db.create_tables([Employee, Vacation], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def addEmployee():
    empnum = int(input("Enter Employee Number > "))
    lstnm = input("Enter Employee Last Name > ")
    fstnm = input("Enter Employee First Name > ")
    hrdt = input("Enter Date of Hire --MM/DD/YYYY-- > ")
    pwd = input("Enter User Password > ")
    pwd2 = input("Re-enter Password > ")
    while pwd != pwd2:
        print("Password Mismatch...try again")
        pwd = input("Enter User Password > ")
        pwd2 = input("Re-enter Password > ")
    clear()
    print('Adding Employee to Database...')
    Employee.create(employeeNumber=empnum, lastName=lstnm, firstName=fstnm, hireDate=hrdt, password=pwd)
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


def scheduleVacation():
    empnum = int(input('Enter Employee Number > '))
    numdays = int(input('Enter Total Days Requested > '))
    if numdays >= 1:
        strtdte = input('Enter Start Date --MM/DD/YYYY-- > ')
        strtdteF = dateConvert(strtdte)
        countdwn = numdays
        Vacation.create(employeeNumber=empnum, vacationDate=strtdte, hoursUsed=8)

