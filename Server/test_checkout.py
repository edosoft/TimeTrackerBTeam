from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime

from messages import CheckoutResponseMessage
from models import User, Workday


def checkout(self, request, date):
        # A function which updates the Workday with the check out date and the total hours
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


# [START Check Out Tests]
    def testcheckoutok(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15, minute=30)
        work = Workday(employeeid="lelele", date=date, checkin=date, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "Checkout Ok. Have a nice day :)")

    def testcheckoutearly(self):
        date = datetime.datetime.now().replace(hour=11)
        work = Workday(employeeid="lelele", date=date, checkin=date, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "You checked out too early")

    def testcheckoutlate(self):
        date = datetime.datetime.now()
        date = date.replace(hour=20)
        work = Workday(employeeid="lelele", date=date, checkin=date, checkout=None, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "Check out out of time")

    def testcheckoutwithanother(self):
        date = datetime.datetime.now()
        date = date.replace(hour=15)
        work = Workday(employeeid="lelele", date=date, checkin=date, checkout=date, total=0)
        work.put()
        test = User(email="lelele")
        result = checkout(self, test, date)
        self.assertEqual(result.text, "You can't check out if you checked out already")
# [END   Check Out Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
