from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import calendar
import datetime

from messages import CheckinResponseMessage
from models import User, Workday

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

# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]