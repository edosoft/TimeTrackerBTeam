#!/usr/bin/env python

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import calendar
from datetime import datetime, timedelta

from messages import ReportMessage, ReportResponseMessage, WorkdayMessage
from models import User, Workday

from reports import get_report
from login import log_in

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
        first = "2017-W34"
        result = get_report(first, 0)
        self.assertEqual(result.text, "There are no records in the selected date")
        self.assertEqual(type(result), ReportResponseMessage)

    def test_get_report_ok(self):
        first ="2017-W45"
        user1 = User(email="user@edosoft.es")
        user1.put()

        for x in range(6, 11):
            date = datetime.now().replace(month = 11, day = x)
            work = Workday(employee=user1,date=date, total=480)
            work.put()

        result = get_report(first, 0)
        self.assertEqual(len(User.query().fetch(10)), 1, "More than one user found")
        self.assertEqual(len(Workday.query().fetch(10)), 5, "Not all Workday created")
        self.assertTrue(len(result.reports) > 0, "No report created")
        self.assertTrue(len(result.reports) == 1, "More than one report found")
        self.assertEqual(result.reports[0].email, "user@edosoft.es", "Invalid user found")
        self.assertEqual(result.reports[0].workday[0].total, 480, "Bad data stored")
        self.assertEqual(result.reports[0].workday[1].total, 480, "Bad data stored")
        self.assertEqual(result.reports[0].total, 2400, "Total data not found:")

    def test_get_report(self):
        user1 = User(email="user@edosoft.es")
        user1.put()
        user2 = User(email="hmr@edosoft.es")
        user2.put()
        date = datetime.now().replace(month = 11,day = 5)
        work = Workday(employee=user1,date=date, total=300)
        work.put()
        for x in range(21, 23):
            date = datetime.now().replace(month = 11,day = x)
            work = Workday(employee=user1,date=date, total=300)
            work.put()

        date = datetime.now().replace(month = 11,day = 23)
        work = Workday(employee=user1,date=date, total=500)
        work.put()

        for x in range(20, 24):
            date = datetime.now().replace(month = 11,day = x)
            work = Workday(employee=user2,date=date, total=480)
            work.put()

        first = "2017-11"

        result = get_report(first, 1)
        self.assertEqual(len(User.query().fetch(10)), 2)
        self.assertEqual(len(result.reports), 2)
        self.assertEqual(result.reports[0].email, "user@edosoft.es")
        self.assertEqual(result.reports[1].email, "hmr@edosoft.es")
        self.assertEqual(result.reports[0].total, 1400, "Wrong total hours for #1")
        self.assertEqual(result.reports[1].total, 32*60, "Wrong total hours for #2")
        self.assertEqual(len(Workday.query().fetch(10)), 8)
        self.assertEqual(result.reports[0].total_days_worked, 4, "Bad count of days")
        self.assertEqual(result.reports[1].total_days_worked, 4, "Bad count of days")

# [END   Report Tests]


if __name__ == '__main__':
    unittest.main()
