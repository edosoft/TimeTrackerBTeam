#!/usr/bin/env python

import endpoints
import datetime

from login import log_in
from checkin import check_in
from checkout import check_out
from reports import get_report
from issues import get_user_with_issues

import util

from tasks import automatic_checkout_helper

from protorpc import message_types
from protorpc import remote

from messages import WorkdayResponseMessage, CheckinResponseMessage, CheckoutResponseMessage
from messages import RequestReport, ReportResponseMessage, WeekTotalMessage , IssueResponseMessage, RequestCurrentDate, CurrentDateResponseMessage

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

    @endpoints.method(RequestReport, ReportResponseMessage,
                      path='report', http_method='POST', name='report')
    def report(self, request):
        """
        A function which updates the Workday with the checkout date and the total hours.
        If the checkout is made in a valid time, the system returns updates the Workday entity
        with the checkout date and total. If not, the system returns an error or raises an issue
        if necessary
        """

        # user = endpoints.get_current_user()
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

app = endpoints.api_server([MainPage], restricted=False)
