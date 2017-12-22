from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime
import admin

from messages import WorkdayResponseMessage
from models import User, Workday
from login import log_in
# [END imports]

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
        self.user = User(email="hrm@edosoft.es")
        self.date = datetime.datetime.now()

# [START Workday Tests]
    def test_workday_no_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        result = log_in(None, date)
        self.assertEqual(result.text, "Error: Invalid Data")

    def test_workday_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        test = User(email="lelele@edosoft.es")
        result = log_in(test, date)
        self.assertEqual(result.text, "Creating Workday")

    def test_workday_returning_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        test = User(email="lelele@edosoft.es")
        log_in(test, date)
        result = log_in(test, date)
        self.assertEqual(result.text, "Returning Workday")
        self.assertEqual(len(Workday.query().fetch(2)), 1)

    def test_workday_multiple_user(self):
        date = datetime.datetime.now()
        test = User(email="lelele@edosoft.es")
        log_in(test, date)
        date = date.replace(hour=7, minute=31)
        result = log_in(test, date)
        self.assertEqual(result.text, "Returning Workday")
        self.assertEqual(len(Workday.query().fetch(2)), 1)
# [END   Workday Tests]

# [START User Tests]
    def test_user(self):
        date = datetime.datetime.now()
        result = log_in(self.user, date)
        self.assertEqual(result.text, "Creating Workday")

    def test_returning_user(self):
        date = datetime.datetime.now()
        log_in(self.user, date)
        result = log_in(self.user, date)
        self.assertEqual(result.text, "Returning Workday")

    def test_multiple_user(self):
        date = datetime.datetime.now()
        log_in(self.user, date)
        log_in(User(email="lelele@edosoft.es"), date)
        result = log_in(User(email="lelele2@edosoft.es"), date)
        self.assertEqual(3, len(User.query().fetch(10)))
# [END   User Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
