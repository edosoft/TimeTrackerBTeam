#!/usr/bin/env python

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest

from messages import GetUserListMessage, GetUserListResponseMessage
from messages import RequestChangeRole, ChangeRoleResponseMessage
from models import User

from admin import get_user_list, change_role

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

# [START Report Tests]
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
        self.assertEqual(result.user_list[0].email, "hrm@edosoft.es", "Invalid user found")
        self.assertEqual(result.user_list[0].name, "Helena Heras", "Invalid user found")
        self.assertEqual(result.user_list[0].hrm, 1, "Invalid user found")
        self.assertEqual(result.user_list[0].admin, 0, "Invalid user found")
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

# [END   Report Tests]


if __name__ == '__main__':
    unittest.main()
