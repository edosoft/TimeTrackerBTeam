#!/usr/bin/env python
#Calling: python runner.py ~/google/google-cloud-sdk/platform/google_appengine
# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import calendar
import datetime

from messages import WorkdayResponseMessage, CheckinResponseMessage, CheckoutResponseMessage, WeekResponseMessage, WeekReportMessage
from models import User, Workday
# [END imports]

def get_report(self, first, last):
    '''A function which returns the reports of a selected week '''
    #print(map(lambda x: x.date.isocalendar()[2], q))
    queryWork = Workday.query(Workday.date >= first, Workday.date < last)
    if len(queryWork.fetch(2)) < 1:
        return WeekResponseMessage(response_code=400, text="There are no registers at the selected week")
    else:
        queryUser = User.query()
        result = []
        for user in queryUser:
            weekRep = WeekReportMessage()
            weekRep.email=user.email
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

def checkin(self, request, date):
    '''A function which updates the Workday with the check in date'''
    user = request

    querycheckin = Workday.query(Workday.employeeid == user.email,
                                 Workday.date == date).get()

    # querycheckin has the Workday of the employee in the proper day.
    if querycheckin.checkin is None:
        now = date
        checkmin = now.replace(hour=7, minute=30, second=59, microsecond=0)
        checkmax = now.replace(hour=9, minute=00, second=59, microsecond=0)
        if now < checkmin:
            # Error - Check in too soon
            return CheckinResponseMessage(response_code=400,
                                          text="You can't check in before 7:30 am")
        else:
            querycheckin.checkin = now
            querycheckin.put()
            if now < checkmax:
                # Ok
                return CheckinResponseMessage(response_code=200,
                                              text="Successful Check in",
                                              checkin=str(querycheckin.checkin))
            else:
                # Issue - Check in too late.
                return CheckinResponseMessage(response_code=200,
                                              text="Check in out of time",
                                              checkin=str(querycheckin.checkin))
    else:
        # Error - Check in after check in
        return CheckinResponseMessage(response_code=400, text="You can't check in again today")

def checkout(self, request, date):
        #A function which updates the Workday with the check out date and the total hours
        user = request

        querycheckout = Workday.query(Workday.employeeid == user.email,
                                      Workday.date == date).get()

        if querycheckout.checkout is not None:
            # Error - Check out after check out
            return CheckoutResponseMessage(response_code=400,
                                           text="You can't check out if you checked out already")

        if querycheckout.checkin is None:
            # Error - Check out without check in
            return CheckoutResponseMessage(response_code=400,
                                           text="You can't check out without checking in")
        else:
            now = date
            checkmin = now.replace(hour=13, minute=00, second=0, microsecond=0)
            checkmax = now.replace(hour=19, minute=00, second=0, microsecond=0)
            checknoon = now.replace(hour=15, minute=00, second=0, microsecond=0)

            querycheckout.checkout = datetime.datetime.now()
            querycheckout.total = (querycheckout.checkout - querycheckout.checkin).seconds / 60
            if now < checkmin:
                querycheckout.put()
                # Issue - Check out too soon
                return CheckoutResponseMessage(response_code=200,
                                               text="You checked out too early",
                                               checkout=str(querycheckout.checkout),
                                               total=querycheckout.total)
            else:
                if now > checknoon:  # If you go out after 15:00, a hour is substracted from the total
                    querycheckout.total = querycheckout.total - 60

                if now < checkmax:
                    querycheckout.put()
                    # OK
                    return CheckoutResponseMessage(response_code=200,
                                                   text="Checkout Ok. Have a nice day :)",
                                                   checkout=str(querycheckout.checkout),
                                                   total=querycheckout.total)
                else:
                    querycheckout.checkout = checkmax
                    querycheckout.put()
                    # Issue - Check out too late.
                    return CheckoutResponseMessage(response_code=200,
                                                   text="Check out out of time",
                                                   checkout=str(querycheckout.checkout),
                                                   total=querycheckout.total)


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

    # [START datastore_example_insert]
    def testInsertEntity(self):
        User().put()
        self.assertEqual(1, len(User.query().fetch(2)))

    def testentityok(self):
        test = User(email="lelele")
        test.put()
        self.assertEqual("lelele", User.query().get().email)
    # [END datastore_example_insert]

# [START Check In Tests]
    def testcheckinok(self):
        date = datetime.datetime.now()
        date = date.replace(hour=8, minute=30)
        work = Workday(employeeid="lelele",date=date, checkin=None, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkin(self, test, date)
        self.assertEqual(result.text, "Successful Check in")

    def testcheckinearly(self):
        date = datetime.datetime.now().replace(hour=6)
        work = Workday(employeeid="lelele",date=date, checkin=None, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkin(self, test, date)
        self.assertEqual(result.text, "You can't check in before 7:30 am")

    def testcheckinlate(self):
        date = datetime.datetime.now()
        date = date.replace(hour=10)
        work = Workday(employeeid="lelele",date=date, checkin=None, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkin(self, test, date)
        self.assertEqual(result.text, "Check in out of time") 

    def testcheckinwithanother(self):
        date = datetime.datetime.now()
        date = date.replace(hour=10)
        work = Workday(employeeid="lelele",date=date, checkin=date, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkin(self, test, date)
        self.assertEqual(result.text, "You can't check in again today")     
# [END   Check In Tests]

# [START Check Out Tests]
    def testcheckoutok(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15, minute=30)
        work = Workday(employeeid="lelele",date=date, checkin=date, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "Checkout Ok. Have a nice day :)")

    def testcheckoutearly(self):
        date = datetime.datetime.now().replace(hour=11)
        work = Workday(employeeid="lelele",date=date, checkin=date, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "You checked out too early")

    def testcheckoutlate(self):
        date = datetime.datetime.now()
        date = date.replace(hour=20)
        work = Workday(employeeid="lelele",date=date, checkin=date, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "Check out out of time") 

    def testcheckoutwithanother(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15)
        work = Workday(employeeid="lelele",date=date, checkin=date, checkout=date, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "You can't check out if you checked out already")     
# [END   Check Out Tests]

# [START Report Tests]
    def test_get_empty_report(self):
        first =datetime.date(2017, 1, 1)
        last = datetime.date(2017, 1, 8)
        result = get_report(self, first, last)
        self.assertEqual(result.text, "There are no registers at the selected week")
        self.assertEqual(type(result), WeekResponseMessage)

    def test_get_report(self):
        user1 = User(email="lelele")
        user1.put()
        user2 = User(email="alexia")
        user2.put()
        date = datetime.datetime.now().replace(day = 5)
        work = Workday(employeeid="lelele",date=date, checkin=None, checkout=None, total=5)
        work.put()
        date = datetime.datetime.now().replace(day = 21)
        work = Workday(employeeid="lelele",date=date, checkin=None, checkout=None, total=7)
        work.put()
        date = datetime.datetime.now().replace(day = 22)
        work = Workday(employeeid="lelele",date=date, checkin=None, checkout=None, total=7)
        work.put()
        date = datetime.datetime.now().replace(day = 23)
        work = Workday(employeeid="lelele",date=date, checkin=None, checkout=None, total=9)
        work.put()

        date = datetime.datetime.now().replace(day = 20)
        work = Workday(employeeid="alexia",date=date, checkin=None, checkout=None, total=8)
        work.put()
        date = datetime.datetime.now().replace(day = 21)
        work = Workday(employeeid="alexia",date=date, checkin=None, checkout=None, total=8)
        work.put()
        date = datetime.datetime.now().replace(day = 22)
        work = Workday(employeeid="alexia",date=date, checkin=None, checkout=None, total=8)
        work.put()
        date = datetime.datetime.now().replace(day = 23)
        work = Workday(employeeid="alexia",date=date, checkin=None, checkout=None, total=8)
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
   
# [END   Check Out Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]