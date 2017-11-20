#!/usr/bin/env python

import unittest
import datetime
from reports import dataStore, WeekEmployeeData, WeekReport

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

    def test_access_data_in_week(self):
        """Test getting an object from a certain week"""
        week = datetime.date.today()
        number = week.isocalendar()[1]
        emp = WeekEmployeeData("Ernesto", 8, 8, 8, 8, 8, 0, 0)
        week_report = WeekReport(number, emp)
        data = dataStore()
        data.addReport(week_report)
        result = data.get_weekly_report(number)
        self.assertEqual(result.employee, "Ernesto", "No data found")

    def test_access_data_in_week_error(self):
        """Testing trying an object from a week, but giving an error"""
        week = datetime.date.today()
        number = week.isocalendar()[1]
        wrong_number = -15
        emp = WeekEmployeeData("Ernesto", 8, 8, 8, 8, 8, 0, 0)
        week_report = WeekReport(number, emp)
        data = dataStore()
        data.addReport(week_report)
        result = data.get_weekly_report(wrong_number)
        self.assertEqual(result, "There are not registers in the selected week")
        #self.assertEqual(result.data.employee, "Ernesto", "No data found")

    def test_total_hours_worked_over(self):
        """Analyzing the weekdays and filtering the vacation ones"""
        emp = WeekEmployeeData("Ernesto", 8, 8, 8, 8, 9, 0, 0)
        self.assertEqual(emp.validationTotal(), 2)

    def test_total_hours_worked_lesser(self):
        """Analyzing the weekdays and filtering the vacation ones"""
        emp = WeekEmployeeData("Ernesto", 8, 8, 8, 8, 6, 0, 0)
        self.assertEqual(emp.validationTotal(), 1)

if __name__ == '__main__':
    unittest.main()
