from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime

from messages import CheckoutResponseMessage
from models import User, Workday

from checkout import check_out

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


# [START Check Out Tests]
    def testcheckoutok(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15, minute=30)
        test = User(email="lelele")
        work = Workday(employee=test, date=date, checkin=date, checkout=None, total=0)
        work.put()
        result = check_out(test, date)
        self.assertEqual(result.text, "Checkout Ok. Have a nice day :)")

    def testcheckoutearly(self):
        date = datetime.datetime.now().replace(hour=11)
        test = User(email="lelele")
        work = Workday(employee=test, date=date, checkin=date, checkout=None, total=0)
        work.put()
        result = check_out(test, date)
        self.assertEqual(result.text, "You checked out too early")

    def testcheckoutlate(self):
        date = datetime.datetime.now()
        date = date.replace(hour=20)
        test = User(email="lelele")
        work = Workday(employee=test, date=date, checkin=date, checkout=None, total=0)
        work.put()
        result = check_out(test, date)
        self.assertEqual(result.text, "Check out out of time")

    def testcheckoutwithanother(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15)
        test = User(email="lelele")
        work = Workday(employee=test, date=date, checkin=date, checkout=date, total=0)
        work.put()
        result = check_out(test, date)
        self.assertEqual(result.text, "You can't check out if you checked out already")
# [END   Check Out Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
