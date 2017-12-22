from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
from datetime import datetime, date
from models import Workday, User
from tasks import automatic_checkout_helper
from login import log_in
from checkin import check_in
from checkout import check_out
import admin

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

    def test_auto_checkout(self):
        fake_date = datetime.now().replace(hour=8, minute=0)
        fake_user = User(email="hrm@edosoft.es")
        log_in(fake_user, fake_date)
        check_in(fake_user, fake_date)
    
        automatic_checkout_helper()

        queryWorkday = Workday.query(Workday.date == date.today(),
                                     Workday.employee.email == "hrm@edosoft.es").get()
        #print (queryWorkday)
        self.assertTrue(queryWorkday.checkout[-1], "checkout not closed")

    def test_auto_checkout_with_false_checkin(self):
        fake_date = datetime.now()
        fake_user = User(email="hrm@edosoft.es")
        fake_work = Workday(employee=fake_user, date=fake_date,
                            total=0)
        fake_work.put()
        automatic_checkout_helper()

        queryWorkday = Workday.query(Workday.date == date.today(),
                                     Workday.employee.email == "hrm@edosoft.es").get()
        self.assertFalse(queryWorkday.checkout, "checkout not closed")


if __name__ == '__main__':
    unittest.main()
