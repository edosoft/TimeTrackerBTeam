#!/usr/bin/env python

# from google.appengine.api.taskqueue import taskqueue
# from google.appengine.ext import ndb
# from protorpc import message_types
# from protorpc import remote

# TODO

import calendar
import datetime

'''
class WeekEmployeeData(ndb.Model):
    """A main model for representing an individual week of the employee data."""
    employee = ndb.StringProperty(indexed=False)
    monday = ndb.IntegerProperty(indexed=False)
    tuesday = ndb.IntegerProperty(indexed=False)
    wednesday = ndb.IntegerProperty(indexed=False)
    thursday = ndb.IntegerProperty(indexed=False)
    friday = ndb.IntegerProperty(indexed=False)
    saturday = ndb.IntegerProperty(indexed=False)
    sunday = ndb.IntegerProperty(indexed=False)
    total = ndb.IntegerProperty(indexed=False)

class WeekReport(ndb.Model):
    week = ndb.IntegerProperty()
    report = ndb.StructuredProperty(WeekEmployeeData)

'''


class dataStore():
    def __init__(self):
        self.report = []

    def contains(self, workday):
        for element in self.report:
            if element.employeeid == workday.employeeid and element.date == workday.date:
                return True
        return False

    def add(self, workday):
        if self.contains(workday):
            return "Duplicate workday"
        self.report.append(workday)

    def get_weekly_report(self, week):
        result = []
        for element in self.report:
            week_element = element.date.isocalendar()[1]
            if week_element == week:
                result.append(element)
        if len(result) == 0:
            return "There are not registers in the selected week"
        return result

    def get_weekly_data_by_employee(self, employee, year, week):
        rawresult = []
        for element in self.report:
            if element.employeeid == employee:
                year_emp = element.date.year
                week_emp = element.date.isocalendar()[1]
                if year == year_emp and week == week_emp:
                    rawresult.append(element)
        if len(rawresult) == 0:
            return "No data found in that week"
        else:
            correct_result = self.formatDataByWeek(rawresult)
            # correct_result = (rawresult)
        return correct_result

    def formatDataByWeek(self, input):
        result = WeekEmployeeData()
        result.employeeid = input[0].employeeid

        for elem in input:
            date = elem.date
            day_emp = calendar.day_name[date.weekday()]
            if day_emp == "Monday":
                result.setMonday(elem.total)
            elif day_emp == "Tuesday":
                result.setTuesday(elem.total)
            elif day_emp == "Wednesday":
                result.setWednesday(elem.total)
            elif day_emp == "Thursday":
                result.setThursday(elem.total)
            elif day_emp == "Friday":
                result.setFriday(elem.total)
            elif day_emp == "Saturday":
                result.setSaturday(elem.total)
            elif day_emp == "Sunday":
                result.setSunday(elem.total)

        result.setTotal()
        return result


class WeekEmployeeData():
    def __init__(self):
        self.employeeid = ""
        self.monday = 0
        self.tuesday = 0
        self.wednesday = 0
        self.thursday = 0
        self.friday = 0
        self.saturday = 0
        self.sunday = 0
        self.total = 0

    def setMonday(self, monday):
        self.monday = monday

    def setTuesday(self, tuesday):
        self.tuesday = tuesday

    def setWednesday(self, wednesday):
        self.wednesday = wednesday

    def setThursday(self, thursday):
        self.thursday = thursday

    def setFriday(self, friday):
        self.friday = friday

    def setSaturday(self, saturday):
        self.saturday = saturday

    def setSunday(self, sunday):
        self.sunday = sunday

    def setTotal(self):
        self.total = self.monday + self.tuesday + self.wednesday + self.thursday + self.friday + self.saturday + self.sunday

    def validationTotal(self):
        """If 2, +40 hours worked. If 1, -40 hours worked. If 0, okay"""
        if self.total > 40:
            return 2
        elif self.total < 40:
            return 1
        else:
            return 0


class Workday():
    def __init__(self):
        self.employeeid = ""
        self.date = datetime.date(1970, 1, 1)
        self.checkin = datetime.date(1970, 1, 1)
        self.checkout = datetime.date(1970, 1, 1)
        self.total = 0

    def getId(self):
        return self.employeeid

    def getDate(self):
        return self.date

    def getCheckin(self):
        return self.checkin

    def getCheckout(self):
        return self.checkout

    def getTotal(self):
        return self.total

    def setEmployee(self, employeeid):
        self.employeeid = employeeid

    def setDate(self, date):
        self.date = date

    def setCheckin(self, checkin):
        self.checkin = checkin

    def setCheckout(self, checkout):
        self.checkout = checkout
        self.total = (self.checkout - self.checkin).seconds / 3600
