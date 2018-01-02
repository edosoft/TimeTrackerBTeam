#!/usr/bin/env python

import endpoints
import datetime
from time import sleep

from login import log_in
from checkin import check_in
from checkout import check_out
from reports import get_report
from issues import get_user_with_issues

import util
import admin

from tasks import automatic_checkout_helper

from protorpc import message_types
from protorpc import remote

from messages import WorkdayResponseMessage, CheckinResponseMessage, CheckoutResponseMessage
from messages import RequestReport, ReportResponseMessage, WeekTotalMessage , IssueResponseMessage, RequestCurrentDate, CurrentDateResponseMessage
from messages import RequestChangeRole, ChangeRoleResponseMessage, RequestCurrentDate, CurrentDateResponseMessage
from messages import GetUserListResponseMessage, GetUserListMessage

from models import User, Workday


# v1 will be deprecated by Aug-2018, but it can be used for educational purposes
@endpoints.api(name='timetrackerApi', version='v1',
               allowed_client_ids=["368116371345-ott8mvobq0aqcd8dvpu40b5n2fdjgs8v.apps.googleusercontent.com"],
               scopes=[endpoints.EMAIL_SCOPE])
class MainPage(remote.Service):

    @endpoints.method(message_types.VoidMessage, WorkdayResponseMessage, path='login',
                      http_method='POST', name='login')
    def login(self, request):
        """
        A function which validates the login. It creates a new User if it doesn't exist in the DB,
        and new Workday entities if the valid user hasn't logged in that day. If it's a returning user,
        this function returns the created Workday, and doesn't create a new User.
        Needs - User verified by Google.
        Returns - WorkdayResponseMessage.
        """
        admin.create_user()
        sleep(0.5)

        #workday_query = Workday.query(Workday.employee.email == "hrm@edosoft.es").get()
        #if workday_query is None:
        #    util.create_mock_user()
        
        user = endpoints.get_current_user()
        return log_in(user)

    @endpoints.method(message_types.VoidMessage, CheckinResponseMessage, path='checkin',
                      http_method='POST', name='checkin')
    def checkin(self, request):
        """
        A function which updates the Workday with the check in date. If the check in button
        is pressed in a valid time, the system updates the Workday entity with the date. If not,
        the function returns an error, or raises an Issue if necessary.
        Needs - A valid date
        Returns - CheckinResponseMessage
        """

        user = endpoints.get_current_user()
        return check_in(user)

    @endpoints.method(message_types.VoidMessage, CheckoutResponseMessage,
                      path='checkout', http_method='POST', name='checkout')
    def checkout(self, request):
        """A function which updates the Workday with the checkout date and the total hours.
        If the checkout is made in a valid time, the system returns updates the Workday entity
        with the checkout date and total. If not, the system returns an error or raises an issue
        if necessary
        """

        user = endpoints.get_current_user()
        return check_out(user)

    @endpoints.method(message_types.VoidMessage, WeekTotalMessage,
                      path='weektotal', http_method='POST', name='weektotal')
    def weektotal(self, request):
        """
        Get total worked hours this week
        """

        user = endpoints.get_current_user()
        return util.get_week_total(user)

    @endpoints.method(message_types.VoidMessage, message_types.VoidMessage,
                      path='autocheckout', http_method='GET', name='autocheckout')
    def automatic_checkout(self, request):
        """
        Helper for the cron task to close all pending checkouts
        """

        automatic_checkout_helper()
        return message_types.VoidMessage()

    @endpoints.method(RequestCurrentDate, CurrentDateResponseMessage,
                      path='date', http_method='POST', name='date')
    def date(self, request):
        """
        A function which retuns the current week and the current month with the 
        apropiate format to use in calendar. This function don't return any error.
        """
        return util.current_date(request.report_type)

    @endpoints.method(RequestChangeRole, ChangeRoleResponseMessage,
                      path='change_role', http_method='POST', name='change_role')
    def change_role(self, request):
        """
        A function which change the role in an employee.
        This function don't return any error.
        """
        print(endpoints.get_current_user().email())
        return admin.change_role(request.user_email, request.hrm_value, request.admin_value,endpoints.get_current_user().email())

    @endpoints.method(message_types.VoidMessage, GetUserListResponseMessage,
                        path='user_list', http_method='POST', name='user_list')
    def user_list(self, request):
        """
        A function which returns a users list. This list has email, name, hrm value 
        and admin value of all employee.
        """

        return admin.get_user_list()

    @endpoints.method(RequestReport, ReportResponseMessage,
                      path='report', http_method='POST', name='report')
    def report(self, request):
        """
        A function which returns the reports of a selected date. It returns the user, 
        total hours per day and total hours in the range of selected dates. 
        Needs - The date and the type of the report
        Returns - ReportResponseMessage, an array of ReportMessages
        """

        return get_report(request.date, request.report_type)



    @endpoints.method(message_types.VoidMessage, CheckinResponseMessage,
                      path='create', http_method='POST', name='create')
    def create(self, request):
        """
        An auxiliar function which creates mock users
        """

        return util.create_mock_user()

    @endpoints.method(message_types.VoidMessage, IssueResponseMessage, path='issues', http_method='POST', name='issues')
    def issues(self, request):
        '''
        A function who will get issues
        '''
        return get_user_with_issues()

    @endpoints.method(message_types.VoidMessage, RequestChangeRole, path='currentuser', http_method='POST', name='currentuser')
    def get_current_user(self, request):
        '''
        A function who will return the user HRM and admin value.
        '''
        user = endpoints.get_current_user().email()
        user_data = User.query(User.email == user).get()
        return RequestChangeRole(user_email = user, hrm_value = user_data.hrm, admin_value = user_data.admin)

app = endpoints.api_server([MainPage], restricted=False)
