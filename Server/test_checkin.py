from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime

from messages import CheckinResponseMessage
from models import User, Workday

from checkin import check_in


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
        user = User(email="lelele")
        work = Workday(employee=user, date=date, checkin=None, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = check_in(test, date)
        self.assertEqual(result.text, "Successful Check in")

    def testcheckinearly(self):
        test = User(email="lelele")
        date = datetime.datetime.now().replace(hour=6)
        work = Workday(employee=test, date=date, checkin=None, checkout=None, total=0)
        work.put()
        result = check_in(test, date)
        self.assertEqual(result.text, "You can't check in before 7:30 am")

    def testcheckinlate(self):
        test = User(email="lelele")
        date = datetime.datetime.now()
        date = date.replace(hour=10)
        work = Workday(employee=test, date=date, checkin=None, checkout=None, total=0)
        work.put()
        result = check_in(test, date)
        self.assertEqual(result.text, "Check in out of time")

    def testcheckinwithanother(self):
        date = datetime.datetime.now()
        date = date.replace(hour=10)
        test = User(email="lelele")
        work = Workday(employee=test, date=date, checkin=date, checkout=None, total=0)
        work.put()
        result = check_in(test, date)
        self.assertEqual(result.text, "You can't check in again today")
# [END   Check In Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
