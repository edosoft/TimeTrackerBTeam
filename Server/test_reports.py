#!/usr/bin/env python

import unittest
import datetime
import calendar
from reports import dataStore, Workday

class TestReport(unittest.TestCase):
    '''Class to test the different cases of report'''
    '''
    Given a HRM trying to access a week where there is no data:
    The system shows an error: 'There are not registers in the selected week'
    Given a HRM accessing a valid week with data:
    The system returns: a list of employees,
                        their hours per day value
                        and a total value per week,
    showing the row with a different color if the weekly limit has not been reached.
    Also, vacation days have to be shown on in a different way:
    The weekly limit will change if h/w worked < workdaysx8.
    Given a HRM accessing a valid week:
    The system returns the previous weekly report, in order to not show empty data.
    '''
    
    def setUp(self):
        self.data = dataStore()
        self.date = datetime.date(2017, 10, 25)
        self.number = self.date.isocalendar()[1]
        self.checkin = datetime.datetime(2017, 10, 25, 8, 20)
        self.checkout = datetime.datetime(2017, 10, 25, 15, 20)
        self.employee = Workday()
        self.employee.setCheckin(self.checkin)
        self.employee.setCheckout(self.checkout)

        self.employee1 = Workday()
        self.employee1.setEmployee("Juan")
        self.employee1.setDate(self.date)
        self.employee1.setCheckin(self.checkin)
        self.employee1.setCheckout(self.checkout)

        employee2 = Workday()
        employee2.setEmployee("Ana")
        employee2.setDate(datetime.date(2017, 10, 26))
        employee2.setCheckin(datetime.datetime(2017, 10, 26, 8, 20))
        employee2.setCheckout(datetime.datetime(2017, 10, 26, 15, 20))

        employee3 = Workday()
        employee3.setDate(self.date)
        employee3.setEmployee("Carlos")
        employee3.setCheckin(self.checkin)
        employee3.setCheckout(self.checkout)

        employee4 = Workday()
        employee4.setEmployee("Juan")
        employee4.setDate(datetime.date(2017, 10, 26))
        employee4.setCheckin(datetime.datetime(2017, 10, 26, 8, 20))
        employee4.setCheckout(datetime.datetime(2017, 10, 26, 15, 20))

        employee5 = Workday()
        employee5.setEmployee("Juan")
        employee5.setDate(datetime.date(2017, 10, 27))
        employee5.setCheckin(datetime.datetime(2017, 10, 27, 8, 20))
        employee5.setCheckout(datetime.datetime(2017, 10, 27, 15, 20))

        self.data.add(self.employee1)
        self.data.add(employee2)
        self.data.add(employee3)
        self.data.add(employee4)
        self.data.add(employee5)

    def test_create_workday(self):
        """Create a workday, add it to the database, test it"""
        self.assertEqual(self.employee.getTotal(), 7)

    def test_access_workday_in_week(self):
        """Test getting an object from a certain week identified by number"""

        result = self.data.get_weekly_report(self.number)
        self.assertEqual(result[0].getId(), "Juan", "No data found")
        self.assertEqual(result[1].getTotal(), 7, "No data found")
        self.assertEqual(result[1].getId(), "Ana", "No data found")

    def test_access_data_in_week_error(self):
        """Testing trying an object from a week, but giving an error"""
        wrong_number = -15
        self.assertEqual(self.data.get_weekly_report(wrong_number), "There are not registers in the selected week")
        #self.assertEqual(result.data.employee, "Ernesto", "No data found")

    def test_get_report_from_employee(self):
        """Test getting an object from a certain week"""
        basedate = datetime.date(2017, 10, 25)
        year_number = basedate.year
        week_number = basedate.isocalendar()[1]

        result = self.data.get_weekly_data_by_employee("Juan", year_number, week_number)
        self.assertEqual(result.employeeid, "Juan", "No data found")
        self.assertEqual(result.wednesday, 7)
        self.assertEqual(result.total, 21, "No data found")


    def test_insert_duplicate_data(self):
        employee6 = self.employee1

        self.assertEqual(self.data.add(employee6), "Duplicate workday")
'''
    def test_total_hours_worked_over(self):
        """Analyzing the weekdays and filtering the vacation ones"""
        
        self.assertEqual(emp.validationTotal(), 2)

    def test_total_hours_worked_lesser(self):
        """Analyzing the weekdays and filtering the vacation ones"""
        
        self.assertEqual(emp.validationTotal(), 1)
'''
if __name__ == '__main__':
    unittest.main()
