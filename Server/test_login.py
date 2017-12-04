from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime

from messages import WorkdayResponseMessage
from models import User, Workday
# [END imports]


def login(self, request, date):
    '''A function which validates the login. It creates User and Workday entities '''
    user = request

    if user is None:
        # Error - Logging without authenticating with Google
        return WorkdayResponseMessage(text="Error: Invalid Data", response_code=400)
    else:
        query = User.query(User.email == user.email).get()
        # If the user doesn't exist, it inserts it to the database.
        if query is None:
            auth = User(email=user.email)
            auth.put()

        queryworkday = Workday.query(Workday.employee.email == user.email,
                                     Workday.date == date).get()

        if queryworkday is None:
            # If there is no workday, a new one is created and added to the DB.
            work = Workday()
            work.employee = User(email=user.email)
            work.checkin = None
            work.checkout = None
            work.total = 0
            work.put()

            # Ok - Creating workday
            return WorkdayResponseMessage(text="Creating Workday", employee=work.employee.email,
                                          date=str(work.date), checkin=str(work.checkin),
                                          checkout=str(work.checkout), total=work.total,
                                          response_code=200)
        else:
            work = queryworkday

            # Ok - Returning existent
            return WorkdayResponseMessage(text="Returning Workday", employee=work.employee.email,
                                          date=str(work.date), checkin=str(work.checkin),
                                          checkout=str(work.checkout), total=work.total,
                                          response_code=200)


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

# [START Workday Tests]
    def test_workday_no_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        result = login(self, None, date)
        self.assertEqual(result.text, "Error: Invalid Data")

    def test_workday_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        test = User(email="lelele")
        result = login(self, test, date)
        self.assertEqual(result.text, "Creating Workday")

    def test_workday_returning_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        test = User(email="lelele")
        login(self, test, date)
        result = login(self, test, date)
        self.assertEqual(result.text, "Returning Workday")
        self.assertEqual(len(Workday.query().fetch(2)), 1)

    def test_workday_multiple_user(self):
        date = datetime.datetime.now()
        test = User(email="lelele")
        login(self, test, date)
        date = date.replace(hour=7, minute=31)
        result = login(self, test, date)
        self.assertEqual(result.text, "Returning Workday")
        self.assertEqual(len(Workday.query().fetch(2)), 1)
# [END   Workday Tests]

# [START User Tests]
    def test_user(self):
        date = datetime.datetime.now()
        result = login(self, User(), date)
        self.assertEqual(result.text, "Creating Workday")

    def test_multiple_user(self):
        date = datetime.datetime.now()
        result = login(self, User(), date)
        result = login(self, User(email="lelele"), date)
        result = login(self, User(email="lelele2"), date)
        self.assertEqual(3, len(User.query().fetch(10)))
# [END   User Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
