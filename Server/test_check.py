from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime
import admin

from messages import CheckinResponseMessage, CheckoutResponseMessage
from models import User, Workday

from checkin import check_in
from login import log_in
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
        admin.create_user()

# [END datastore_example_test]

    # [START datastore_example_teardown]
    def tearDown(self):
        self.testbed.deactivate()
    # [END datastore_example_teardown]

# [START Check In Tests]
    def testcheckinok(self):
        date = datetime.datetime.now()
        date = date.replace(hour=8, minute=30)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date)
        result = check_in(user, date)
        self.assertEqual(result.text, "Successful Check in")
        self.assertEqual(result.number,1)

    def testcheckinearly(self):
        date = datetime.datetime.now().replace(hour=6)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date)
        result = check_in(user, date)
        self.assertEqual(result.text, "You can't check in before 7:30 am")
    
    def testcheckinlate(self):
        date = datetime.datetime.now()
        date = date.replace(hour=10)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date)
        result = check_in(user, date)
        self.assertEqual(result.text, "Check in out of time")

    def test_checkin_double_no_checkout(self):
        date = datetime.datetime.now()
        date_in = date.replace(hour=8)
        date_out = date.replace(hour=9)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date)
        check_in(user, date_in)
        result = check_in(user, date_out)
        self.assertEqual(result.text, "You can't check in again without checking out before")

    def testmultiplecheckin(self):
        date = datetime.datetime.now()
        date_in = date.replace(hour=8)
        date_out = date.replace(hour=9)

        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        check_in(user, date_in)
        check_out(user, date_out)

        new_date_in = date.replace(hour=11)
        new_date_out = date.replace(hour=12)

        check_in(user, new_date_in)
        check_out(user, new_date_out)

        new_new_date_in = date.replace(hour=15)
        result_in = check_in(user, new_new_date_in)
        self.assertEqual(result_in.text, "Successful Check in")
        self.assertEqual(result_in.number, 3, "Invalid count of check ins")

        new_new_date_out = date.replace(hour=16)
        result_out = check_out(user, new_new_date_out)
        self.assertEqual(result_out.text, "Successful Check out")
        self.assertEqual(result_out.number, 3, "Invalid count of check outs")
       
# [END   Check In Tests]
    
# [START Check Out Tests]

    def test_check_out_without_check_in(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15, minute=30)
        date_in = date.replace(hour=15)
        date_out = date.replace(hour=16)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        result = check_out(user, date_out)
        self.assertEqual(result.text, "You can't check out without checking in")

    def test_multiple_check_out_without_check_in(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15, minute=30)
        date_in = date.replace(hour=15, minute=0)
        date_out = date.replace(hour=16, minute=0)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        check_in(user, date_in)
        early_result = check_out(user, date)
        self.assertEqual(early_result.number, 1, "Wrong checkout number")
        result = check_out(user, date_out)
        self.assertEqual(result.text, "You can't check out without checking in")

    def testcheckoutok(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15, minute=30)
        date_in = date.replace(hour=15)
        date_out = date.replace(hour=16)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        check_in(user, date_in)
        result = check_out(user, date_out)
        self.assertEqual(result.text, "Successful Check out")

    def testcheckoutearly(self):
        date = datetime.datetime.now().replace(hour=11)
        date_in = date.replace(hour=8)
        date_out = date.replace(hour=9)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        check_in(user, date_in)
        result = check_out(user, date_out)
        self.assertEqual(result.text, "You checked out too early")

    def testcheckoutlate(self):
        date = datetime.datetime.now()
        date = date.replace(hour=20)
        date_in = date.replace(hour=15)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        check_in(user, date_in)
        result = check_out(user, date)
        self.assertEqual(result.text, "Check out out of time")

    def test_check_out_when_check_in_soon(self):
        date = datetime.datetime.now()
        date_in = date.replace(hour=8, minute=0)
        date_out = date.replace(hour=8, minute=3)

        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        check_in(user, date_in)

        result = check_out(user, date_out)
        self.assertEqual(result.text, "You can't check out until 5 minutes have passed")
# [END   Check Out Tests]

    def test_returning_workday(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15, minute=30)
        date_in = date.replace(hour=15)
        date_out = date.replace(hour=16)
        user = User(email="maria.ramos@edosoft.es")
        log_in(user, date_in)
        check_in(user, date_in)
        check_out(user, date_out)
        log_in(user, date_in)
        check_in(user, date_in)
        check_out(user, date_out)
        result = log_in(user, date_in)
        self.assertEqual(result.text, "Returning Workday")
    
# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
