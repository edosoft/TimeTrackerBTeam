#!/usr/bin/env python

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import calendar
from datetime import datetime, timedelta

from messages import ReportMessage, ReportResponseMessage, WorkdayMessage
from models import User, Workday


def get_report(date, isMonthly=None):
    '''A function which returns the reports of a selected date. It returns the user, 
    total hours per day and total hours in the range. 
    Needs - The date and last day to check
    Returns - ResponseMessage, an array of ReportMessages '''
    #print(map(lambda x: x.date.isocalendar()[2], q))
    #AQUI
    first_date = datetime.strptime(date, "%Y-%m-%d").date()
    cal = calendar.monthrange(first_date.year, first_date.month)
    if isMonthly == "True":
        start_date = first_date.replace(day=1)
        end_date = first_date.replace(day=cal[1])
    else:
        start_date = first_date - timedelta(days=first_date.weekday())
        end_date = start_date + timedelta(days=6)

    requested_workdays = Workday.query(Workday.date >= start_date, Workday.date <= end_date)

    if len(requested_workdays.fetch(10)) < 1:
        return ReportResponseMessage(response_code=400, text="There are no records in the selected date")
    else:
        all_users = User.query()
        result = []
        for user in all_users:
            report_employee = ReportMessage()
            total_hours_per_employee = []
            report_employee.email = user.email
            workdays_by_employee = requested_workdays.filter(
                Workday.employee.email == report_employee.email).order(+Workday.date)
            for elem in workdays_by_employee:
                date_workday = str(elem.date);
                day_of_week = elem.date.isocalendar()[2]
                report_employee.workday.append(WorkdayMessage(date=date_workday, day_of_week=day_of_week,
                                                              total=elem.total))
                total_hours_per_employee.append(elem.total)

            if isMonthly == "True":
                report_employee.total_days_worked = len(workdays_by_employee.fetch())

            report_employee.total = sum(total_hours_per_employee)
            if len(workdays_by_employee.fetch()):
                result.append(report_employee)
        return ReportResponseMessage(response_code=200, text="Returning report", reports=result, month = cal[1])


# [START datastore_example_test]
class DatastoreTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

# [END datastore_example_test]

    # [START datastore_example_teardown]
    def tearDown(self):
        self.testbed.deactivate()
    # [END datastore_example_teardown]

# [START Report Tests]
    def test_get_empty_report(self):
        first = "2017-11-1"
        result = get_report(first, "No")
        self.assertEqual(result.text, "There are no records in the selected date")
        self.assertEqual(type(result), ReportResponseMessage)

    def test_get_report_ok(self):
        first ="2017-11-8"
        user1 = User(email="user@edosoft.es")
        user1.put()

        for x in range(6, 11):
            date = datetime.now().replace(month = 11, day = x)
            work = Workday(employee=user1,date=date, checkin=None, checkout=None, total=7)
            work.put()

        result = get_report(first, "No")
        self.assertEqual(len(User.query().fetch(10)), 1, "More than one user found")
        self.assertEqual(len(Workday.query().fetch(10)), 5, "Not all Workday created")
        self.assertTrue(len(result.reports) > 0, "No report created")
        self.assertTrue(len(result.reports) == 1, "More than one report found")
        self.assertEqual(result.reports[0].email, "user@edosoft.es", "Invalid user found")
        self.assertEqual(result.reports[0].workday[0].total, 7, "Bad data stored")
        self.assertEqual(result.reports[0].workday[1].total, 7, "Bad data stored")
        self.assertEqual(result.reports[0].total, 35, "Total data not found:")
        self.assertEqual(result.reports[0].total_days_worked, None, "Bad count of days")

    def test_get_report(self):
        user1 = User(email="user@edosoft.es")
        user1.put()
        user2 = User(email="hmr@edosoft.es")
        user2.put()
        date = datetime.now().replace(month = 11,day = 5)
        work = Workday(employee=user1,date=date, checkin=None, checkout=None, total=5)
        work.put()
        for x in range(21, 23):
            date = datetime.now().replace(month = 11,day = x)
            work = Workday(employee=user1,date=date, checkin=None, checkout=None, total=15)
            work.put()

        date = datetime.now().replace(month = 11,day = 23)
        work = Workday(employee=user1,date=date, checkin=None, checkout=None, total=10)
        work.put()

        for x in range(20, 24):
            date = datetime.now().replace(month = 11,day = x)
            work = Workday(employee=user2,date=date, checkin=None, checkout=None, total=8)
            work.put()

        first = "2017-11-20"

        result = get_report(first, "True")
        self.assertEqual(len(User.query().fetch(10)), 2)
        self.assertEqual(len(result.reports), 2)
        self.assertEqual(result.reports[0].email, "user@edosoft.es")
        self.assertEqual(result.reports[1].email, "hmr@edosoft.es")
        self.assertEqual(result.reports[0].total, 45, "Wrong total hours for #1")
        self.assertEqual(result.reports[1].total, 32, "Wrong total hours for #2")
        self.assertEqual(len(Workday.query().fetch(10)), 8)
        self.assertEqual(result.reports[0].total_days_worked, 4, "Bad count of days")
        self.assertEqual(result.reports[1].total_days_worked, 4, "Bad count of days")

# [END   Report Tests]


if __name__ == '__main__':
    unittest.main()
