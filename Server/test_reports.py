#!/usr/bin/env python

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime

from messages import WeekReportMessage, WeekResponseMessage
from models import User, Workday


def get_report(self, first, last):
    '''A function which returns the reports of a selected week '''

    # print(map(lambda x: x.date.isocalendar()[2], q))
    queryWork = Workday.query(Workday.date >= first, Workday.date < last)
    if len(queryWork.fetch(2)) < 1:
        return WeekResponseMessage(response_code=400, text="There are no registers at the selected week")
    else:
        queryUser = User.query()
        result = []
        for user in queryUser:
            weekRep = WeekReportMessage()
            weekRep.email = user.email
            weekRep.monday = 0
            weekRep.tuesday = 0
            weekRep.thursday = 0
            weekRep.friday = 0
            weekRep.wednesday = 0
            query_work_by_employee = queryWork.filter(Workday.employeeid == weekRep.email)
            for elem in query_work_by_employee:
                day_emp = elem.date.isocalendar()[2]

                if day_emp == 1:
                    weekRep.monday = elem.total
                elif day_emp == 2:
                    weekRep.tuesday = elem.total
                elif day_emp == 3:
                    weekRep.wednesday = elem.total
                elif day_emp == 4:
                    weekRep.thursday = elem.total
                elif day_emp == 5:
                    weekRep.friday = elem.total

            weekRep.total = weekRep.monday + weekRep.tuesday + weekRep.wednesday + weekRep.thursday + weekRep.friday
            result.append(weekRep)

        return WeekResponseMessage(response_code=200, text="Returning weekly report", reports=result)


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
        first = datetime.date(2017, 1, 1)
        last = datetime.date(2017, 1, 8)
        result = get_report(self, first, last)
        self.assertEqual(result.text, "There are no registers at the selected week")
        self.assertEqual(type(result), WeekResponseMessage)

    def test_get_report(self):
        user1 = User(email="lelele")
        user1.put()
        user2 = User(email="alexia")
        user2.put()
        date = datetime.datetime.now().replace(day=5)
        work = Workday(employeeid="lelele", date=date, checkin=None, checkout=None, total=5)
        work.put()
        date = datetime.datetime.now().replace(day=21)
        work = Workday(employeeid="lelele", date=date, checkin=None, checkout=None, total=7)
        work.put()
        date = datetime.datetime.now().replace(day=22)
        work = Workday(employeeid="lelele", date=date, checkin=None, checkout=None, total=7)
        work.put()
        date = datetime.datetime.now().replace(day=23)
        work = Workday(employeeid="lelele", date=date, checkin=None, checkout=None, total=9)
        work.put()

        date = datetime.datetime.now().replace(day=20)
        work = Workday(employeeid="alexia", date=date, checkin=None, checkout=None, total=8)
        work.put()
        date = datetime.datetime.now().replace(day=21)
        work = Workday(employeeid="alexia", date=date, checkin=None, checkout=None, total=8)
        work.put()
        date = datetime.datetime.now().replace(day=22)
        work = Workday(employeeid="alexia", date=date, checkin=None, checkout=None, total=8)
        work.put()
        date = datetime.datetime.now().replace(day=23)
        work = Workday(employeeid="alexia", date=date, checkin=None, checkout=None, total=8)
        work.put()

        first = datetime.date(2017, 11, 20)
        last = datetime.date(2017, 11, 26)

        result = get_report(self, first, last)
        self.assertEqual(len(User.query().fetch(10)), 2)
        self.assertEqual(len(result.reports), 2)
        self.assertEqual(result.reports[0].email, "lelele")
        self.assertEqual(result.reports[1].email, "alexia")
        self.assertEqual(result.reports[0].total, 23)
        self.assertEqual(len(Workday.query().fetch(10)), 8)
# [END   Report Tests]


if __name__ == '__main__':
    unittest.main()
