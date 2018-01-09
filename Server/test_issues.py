#!/usr/bin/env python

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest

from messages import IssueMessage, IssueResponseMessage, IssuesPerEmployeeMessage
from models import User, Workday, Issue

from issues import get_user_with_issues
from datetime import datetime

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

    def test_employees_without_issues(self):
        user1 = User(email="user@edosoft.es")
        result = get_user_with_issues()
        self.assertEqual(result.response_code, 200)
        self.assertEqual(result.text, 'There aren`t users with issues')

    def test_employees_with_issues(self):
        user1 = User(email="user@edosoft.es")
        user1.put()
        issue1 = Issue(employee=user1, non_viewed=1, non_solved=1, issue_type="Check in late")
        issue1.put()
        result = get_user_with_issues()
        self.assertEqual(result.total_unsolved, 1)
        self.assertEqual(result.response_code, 200)
        self.assertEqual(result.text, 'Returning Issues')

    def test_employees_with_issues(self):
        user1 = User(email="user@edosoft.es")
        user1.put()
        user2 = User(email="aser333@edosoft.es")
        user2.put()
        issue1 = Issue(employee=user1, non_viewed=1, non_solved=1, issue_type="Check in late")
        issue1.put()
        issue2 = Issue(employee=user1, non_viewed=1, non_solved=1, issue_type="Check out late")
        issue2.put()
        issue3 = Issue(employee=user2, non_viewed=1, non_solved=1, issue_type="Check out late")
        issue3.put() 
        result = get_user_with_issues()
        self.assertEqual(result.issues_per_employee[0].total_unsolved_peremp, 2)
        self.assertEqual(result.total_unsolved, 3)
        self.assertEqual(result.response_code, 200)
        self.assertEqual(result.text, 'Returning Issues')

    def test_get_issue(self):
        date = datetime.now()

        user1 = User(email="user@edosoft.es", name='Juan', hrm=0, admin=0)
        user1.put()
        
        wday = Workday()
        cin = []
        cin.append(date)
        wday.employee = user1
        wday.checkin = cin
        wday.checkout = []
        total = 0
        wday.put()

        issue1 = Issue(employee=user1, non_viewed=1, non_solved=1, issue_type="Check in late", created= date.date(), date=date)
        issue1.put()

        result = get_workday_from_issue('user@edosoft.es', date)
        self.assertEqual(result.response_code, 200)
        self.assertEqual(result.workday.employee.name, 'Juan')
        self.assertEqual(result.workday.checkin[0], date)
        self.assertEqual(result.workday.checkout, None)

        # Each time you execute this method, the Issue will change it's non_viewed value to 0. 
        self.assertEqual(issue1.non_viewed, 0)


    def test_get_issue_no_issue(self):
        date = datetime.now()

        user1 = User(email="user@edosoft.es")
        user1.put()
        result = get_workday_from_issue('user@edosoft.es', date)
        self.assertEqual(result.response_code, 400)
        self.assertEqual(result.text, 'No issue found')

    def test_wrong_get_issue_no_user(self):
        date = datetime.now()

        result = get_workday_from_issue('user@edosoft.es', date)
        self.assertEqual(result.response_code, 400)
        self.assertEqual(result.text, 'No user found')


    def test_correct_issue(self):
        date = datetime.now()
        user1 = User(email="user@edosoft.es", name='Juan', hrm=0, admin=0)
        user1.put()
        
        wday = Workday()
        cin = []
        cin.append(date)
        cin.append(date.replace(hour=date.hour+2))
        cin.append(date.replace(hour=date.hour+4))
        cout = []
        cout.append(date.replace(hour=date.hour+1))
        cout.append(date.replace(hour=date.hour+3))
        wday.employee = user1
        wday.checkin = cin
        wday.checkout = cout
        total = 0
        wday.put()

        issue1 = Issue(employee=user1, non_viewed=0, non_solved=1, issue_type="Check in late", created= date.date(), date=date)
        issue1.put()

        correct_cin = []
        correct_cin.append(date)
        correct_cin.append(date)
        correct_cin.append(date)

        correct_cout = correct_cin
        result = correct_issue(user1.email, correct_cin, correct_cout)
        self.assertEqual(result.response_code, 200)
        self.assertEqual(result.text, 'Updated Workday')
        self.assertEqual(issue1.non_solved, 0)