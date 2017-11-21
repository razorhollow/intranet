#!python3
#dbmanager.py - program for manipulating sqlite database

import date

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

class Vacation(BaseModel):
    employeeNumber = IntegerField(primary_key=True,max_length=4, unique=True)
    vacationDate = Datefield(null=False)
    hoursUsed = IntegerField(max_length=1, default=8)

def initialize():
    db.connect()
    db.create_tables([Employee, Vacation], safe=True)
