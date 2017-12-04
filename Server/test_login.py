from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import datetime

from messages import WorkdayResponseMessage
from models import User, Workday
# [END imports]


def login(request, date):
    """
    A function which validates the login. It creates User and Workday entities
    """
    user = request

    if user is None:
        # Error - Logging without authenticating with Google
        return WorkdayResponseMessage(text="Error: Invalid Data", response_code=400)
    else:
        verify_email = user.email.split('@')[1]
        if (verify_email != 'edosoft.es'):
            return WorkdayResponseMessage(text="Error: Invalid Domain", response_code=400)

        user_query = User.query(User.email == user.email).get()
        # If the user doesn't exist, it inserts it to the database.
        if user_query is None:
            auth = User(email=user.email)
            auth.put()

        workday_query = Workday.query(Workday.employee.email == user.email,
                                      Workday.date == date).get()

        if workday_query is None:
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
            work = workday_query

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
        self.user = User(email="email@edosoft.es")
        self.date = datetime.datetime.now()

# [START Workday Tests]
    def test_workday_no_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        result = login(None, date)
        self.assertEqual(result.text, "Error: Invalid Data")

    def test_workday_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        test = User(email="lelele@edosoft.es")
        result = login(test, date)
        self.assertEqual(result.text, "Creating Workday")

    def test_workday_returning_user(self):
        date = datetime.datetime.now()
        date = date.replace(hour=7, minute=31)
        test = User(email="lelele@edosoft.es")
        login(test, date)
        result = login(test, date)
        self.assertEqual(result.text, "Returning Workday")
        self.assertEqual(len(Workday.query().fetch(2)), 1)

    def test_workday_multiple_user(self):
        date = datetime.datetime.now()
        test = User(email="lelele@edosoft.es")
        login(test, date)
        date = date.replace(hour=7, minute=31)
        result = login(test, date)
        self.assertEqual(result.text, "Returning Workday")
        self.assertEqual(len(Workday.query().fetch(2)), 1)
# [END   Workday Tests]

# [START User Tests]
    def test_user(self):
        date = datetime.datetime.now()
        result = login(self.user, date)
        self.assertEqual(result.text, "Creating Workday")

    def test_multiple_user(self):
        date = datetime.datetime.now()
        result = login(self.user, date)
        result = login(User(email="lelele@edosoft.es"), date)
        result = login(User(email="lelele2@edosoft.es"), date)
        self.assertEqual(3, len(User.query().fetch(10)))

    def test_invalid_user(self):
        user_error = User(email="lala@gmail.es")
        result = login(user_error,self.date)
        self.assertEqual(result.text, "Error: Invalid Domain")
        user_ok = User(email="lala@edosoft.es")
        result = login(user_ok,self.date)
        self.assertEqual(result.text, "Creating Workday")
# [END   User Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
