#!/usr/bin/env python

import endpoints
import datetime
from time import sleep

from login import log_in
from checkin import check_in
from checkout import check_out
from reports import get_report
from issues import get_user_with_issues, get_workday_from_issues, correct_issue

import util
import admin

from tasks import automatic_checkout_helper

from protorpc import message_types
from protorpc import remote

from messages import LoginRequest, WorkdayResponseMessage, CheckinResponseMessage, CheckoutResponseMessage
from messages import RequestReport, ReportResponseMessage, WeekTotalMessage , IssueResponseMessage, RequestCurrentDate, CurrentDateResponseMessage
from messages import RequestChangeRole, ChangeRoleResponseMessage, RequestCurrentDate, CurrentDateResponseMessage
from messages import GetUserListResponseMessage, GetUserListMessage, IpMessage,  WorkdayIssueResponseMessage, WorkdayIssueRequestMessage, IssueCorrectionResponseMessage, IssueCorrectionMessage
from messages import IpDateRequest, IpUserRequest, IPDateResponseMessage, IPUserResponseMessage
from models import User, Workday


# v1 will be deprecated by Aug-2018, but it can be used for educational
# purposes
@endpoints.api(name='timetrackerApi', version='v1',
               allowed_client_ids=[
                   "368116371345-ott8mvobq0aqcd8dvpu40b5n2fdjgs8v.apps.googleusercontent.com"],
               scopes=[endpoints.EMAIL_SCOPE])
class MainPage(remote.Service):

    @endpoints.method(LoginRequest, WorkdayResponseMessage, path='login',
                      http_method='POST', name='login')
    def login(self, request):
        """
        A function which validates the login. It creates a new Workday entity if the valid user hasn't logged in that day. If it's a returning user,
        this function returns the created Workday.
        """
        admin.create_user()
        sleep(0.5)

        # workday_query = Workday.query(Workday.employee.email == "hrm@edosoft.es").get()
        # if workday_query is None:
        #    util.create_mock_user()

        user = endpoints.get_current_user()
        return log_in(user, request.name)

    @endpoints.method(IpMessage, CheckinResponseMessage, path='checkin',
                      http_method='POST', name='checkin')
    def checkin(self, request):
        """
        A function which updates the Workday with the check in date. If the check in button
        is pressed in a valid time, the system updates the Workday entity with the date.
        """

        user = endpoints.get_current_user()
        return check_in(user, request.ip)

    @endpoints.method(IpMessage, CheckoutResponseMessage,
                      path='checkout', http_method='POST', name='checkout')
    def checkout(self, request):
        """A function which updates the Workday with the checkout date and the total hours.
        If the checkout is made in a valid time, the system returns updates the Workday entity
        with the checkout date and total.
        """

        user = endpoints.get_current_user()
        return check_out(user, request.ip)

    @endpoints.method(message_types.VoidMessage, WeekTotalMessage,
                      path='weektotal', http_method='POST', name='weektotal')
    def weektotal(self, request):
        """
        A  function which returns the total worked hours of this week.
        """

        user = endpoints.get_current_user()
        return util.get_week_total(user.email())

    @endpoints.method(message_types.VoidMessage, message_types.VoidMessage,
                      path='autocheckout', http_method='GET', name='autocheckout')
    def automatic_checkout(self, request):
        """
        Helper for the cron task to close all pending checkouts
        """

        automatic_checkout_helper()
        return message_types.VoidMessage()

    # UNUSED
    @endpoints.method(message_types.VoidMessage, message_types.VoidMessage,
                      path='testprueba', http_method='GET', name='testprueba')
    def test_prueba(self, request):
        """
        An auxiliar function which creates mock workdays.
        """
        print (datetime.datetime.now())
        return message_types.VoidMessage()

    @endpoints.method(RequestCurrentDate, CurrentDateResponseMessage,
                      path='date', http_method='POST', name='date')
    def date(self, request):
        """
        A function which retuns the current week and the current month with the
        appropiate format to use in calendar.
        """
        return util.current_date(request.report_type)

    @endpoints.method(RequestChangeRole, ChangeRoleResponseMessage,
                      path='change_role', http_method='POST', name='change_role')
    def change_role(self, request):
        """
        A function which updates the roles of an employee.
        """
        print(endpoints.get_current_user().email())
        return admin.change_role(request.user_email, request.hrm_value, request.admin_value, endpoints.get_current_user().email())

    @endpoints.method(message_types.VoidMessage, GetUserListResponseMessage,
                      path='user_list', http_method='POST', name='user_list')
    def user_list(self, request):
        """
        A function which returns the list of users. This list returns the email, name, hrm value
        and admin value of all the employees.
        """

        return admin.get_user_list()

    @endpoints.method(RequestReport, ReportResponseMessage,
                      path='report', http_method='POST', name='report')
    def report(self, request):
        """
        A function which returns the reports of a selected date. It returns the user,
        total hours per day and total hours in the range of selected dates.
        Depending on the type of report (Weekly or Monthly), it also adds the
        total count of days, in the latter case.
        """

        return get_report(request.date, request.report_type)


    @endpoints.method(WorkdayIssueRequestMessage ,WorkdayIssueResponseMessage,
                      path='wissue', http_method='POST', name='wissue')
    def wissue(self, request):
        """
        A function which returns a workday per issue
        """

        return get_workday_from_issues(request.email, request.date, request.issue_type)

    @endpoints.method(message_types.VoidMessage, IssueResponseMessage, path='issues', http_method='POST', name='issues')
    def issues(self, request):
        '''
        A function which returns the list of issues of all the users.
        '''
        return get_user_with_issues()

    @endpoints.method(IpUserRequest, IPUserResponseMessage, path='ip_user', http_method='POST', name='ip_user')
    def get_ips_by_user(self, request):
        '''
        A function which returns the list of issues of all the users.
        '''
        return admin.get_ip_by_user(request.email, request.start_date, request.end_date)

    @endpoints.method(IpDateRequest, IPDateResponseMessage, path='ip_userlist', http_method='POST', name='ip_userlist')
    def get_ips_by_date(self, request):
        '''
        A function which returns the list of issues of all the users.
        '''
        return admin.get_ip_by_date(request.date)

    @endpoints.method(message_types.VoidMessage, RequestChangeRole, path='currentuser', http_method='POST', name='currentuser')
    @endpoints.method(IssueCorrectionMessage, IssueCorrectionResponseMessage,
                      path='correct', http_method='POST', name='correct')
    def correct_issue(self, request):
        '''
        A function which returns the list of issues of all the users.
        '''
        return correct_issue(request.email, request.date, request.issue_type, request.correction)

    @endpoints.method(message_types.VoidMessage, RequestChangeRole,
                      path='currentuser', http_method='POST', name='currentuser')
    def get_current_user(self, request):
        '''
        A function which returns the user HRM and admin value.
        '''
        user = endpoints.get_current_user().email()
        user_data = User.query(User.email == user).get()
        return RequestChangeRole(user_email=user, hrm_value=user_data.hrm, admin_value=user_data.admin)


app = endpoints.api_server([MainPage], restricted=False)
