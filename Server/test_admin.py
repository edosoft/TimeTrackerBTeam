#!/usr/bin/env python

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
from datetime import datetime

from messages import GetUserListMessage, GetUserListResponseMessage
from messages import RequestChangeRole, ChangeRoleResponseMessage
from messages import IPUserResponseMessage, IPUserMessage, IPDateResponseMessage
from models import User, Workday

from admin import get_user_list, change_role, get_user_list, get_ip_by_user, get_ip_by_date

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

# [START UserList Tests]
    def test_get_empty_user_list(self):
        result = get_user_list()
        self.assertEqual(result.text, "Error: Users not found")
        self.assertEqual(type(result), GetUserListResponseMessage)

    def test_get_user_list_ok(self):
        auth1 = User(email="hrm@edosoft.es", name="Helena Heras", admin = 0, hrm = 1)
        auth1.put()
        auth2 = User(email="admin@edosoft.es", name="Antonio Arbelo", admin = 1, hrm = 0)
        auth2.put()

        result = get_user_list()
        self.assertEqual(result.user_list[1].email, "hrm@edosoft.es", "Invalid user found")
        self.assertEqual(result.user_list[1].name, "Helena Heras", "Invalid user found")
        self.assertEqual(result.user_list[1].hrm, 1, "Invalid user found")
        self.assertEqual(result.user_list[1].admin, 0, "Invalid user found")
        self.assertEqual(len(result.user_list), 2, "Wrong size")

    def test_change_role_ok(self):
        auth1 = User(email="hrm@edosoft.es", name="Helena Heras", admin = 0, hrm = 1)
        auth1.put()
        auth2 = User(email="admin@edosoft.es", name="Antonio Arbelo", admin = 1, hrm = 0)
        auth2.put()

        result = change_role(auth1.email, 0,0, auth2.email)
        q=User.query(User.email == auth1.email).get()
        self.assertEqual(q.hrm, 0, "Not changed")
        
    def test_change_own_role_ok(self):
        auth2 = User(email="admin@edosoft.es", name="Antonio Arbelo", admin = 1, hrm = 0)
        auth2.put()

        result = change_role(auth2.email, 1,1, auth2.email)
        q=User.query(User.email == auth2.email).get()
        self.assertEqual(q.hrm, 1, "Not changed")

        result2 = change_role(auth2.email, 1,0, auth2.email)
        q2=User.query(User.email == auth2.email).get()
        self.assertEqual(q2.admin, 1, "Not changed")
        self.assertEqual(result2.text, "You can not change your admin role.")

# [END   UserList Tests]

# [START IP Tests]
    def test_get_empty_ip_by_user_no_user(self):
        date_start = "2018-11-5"
        date_end = "2018-11-6"
        result = get_ip_by_user("cuentaprueba@edosoft.es", date_start, date_end)
        self.assertEqual(result.text, "User doesn't exist")
        self.assertEqual(type(result), IPUserResponseMessage)

    def test_get_empty_ip_by_user_no_data(self):
        user = User(email="user@edosoft.es")
        user.put()
        date_start = "2018-11-5"
        date_end = "2018-11-6"
        result = get_ip_by_user("user@edosoft.es", date_start, date_end)
        self.assertEqual(result.response_code, 400)
        self.assertEqual(result.text, 'There are no records in the selected date')
        self.assertEqual(type(result), IPUserResponseMessage)

    def test_get_ip_by_user_correct(self):
        user = User(email="user@edosoft.es", name="Antonio")
        user.put()

        for x in range(1, 8):
            date = datetime.now().replace(day = x)
            work = Workday(employee=user,date=date, ip_checkin=[str(x), str(x+1)], ip_checkout=[str(x), str(x+1)])
            work.put()

        date_start = str(datetime.now().replace(day=1).date())
        date_end = str(datetime.now().replace(day=7).date())
        result = get_ip_by_user("user@edosoft.es", date_start, date_end)

        self.assertEqual(result.response_code, 200)
        self.assertEqual(result.ip_values[0].ip_checkin, ['1', '2'])
        self.assertEqual(type(result), IPUserResponseMessage)

    def test_get_ip_by_date_correct(self):
        user = User(email="user@edosoft.es", name="Antonio")
        user.put()

        for x in range(1, 8):
            date = datetime.now().replace(day = x)
            work = Workday(employee=user,date=date, ip_checkin=[str(x), str(x+1)], ip_checkout=[str(x), str(x+1)])
            work.put()

        date_start = str(datetime.now().replace(day=1).date())
        result = get_ip_by_date(date_start)
        self.assertEqual(result.response_code, 200)
        self.assertEqual(result.ip_report[0].ip_checkin, ['1', '2'])
        self.assertEqual(type(result), IPDateResponseMessage)

    def test_get_ip_by_date_incorrect(self):
        date_start = str(datetime.now().replace(day=1).date())
        result = get_ip_by_date(date_start)

        self.assertEqual(result.response_code, 400)
        self.assertEqual(type(result), IPDateResponseMessage)

# [END   IP Tests]

if __name__ == '__main__':
    unittest.main()
