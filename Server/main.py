#!/usr/bin/env python

import datetime
import endpoints

import login

from protorpc import message_types
from protorpc import remote

from messages import WorkdayResponseMessage, CheckinResponseMessage, CheckoutResponseMessage

from models import Workday

# v1 will be deprecated by Aug-2018, but it can be used for educational purposes


@endpoints.api(name='timetrackerApi', version='v1',
               allowed_client_ids=["368116371345-ott8mvobq0aqcd8dvpu40b5n2fdjgs8v.apps.googleusercontent.com"],
               scopes=[endpoints.EMAIL_SCOPE])
class MainPage(remote.Service):

    @endpoints.method(message_types.VoidMessage, WorkdayResponseMessage, path='login',
                      http_method='POST', name='login')
    def login(self, request):
        '''A function which validates the login. It creates a new User if it doesn't exist in the DB,
        and new Workday entities if the valid user hasn't logged in that day. If it's a returning user,
        this function returns the created Workday, and doesn't create a new User.
        Needs - User verified by Google.
        Returns - WorkdayResponseMessage. '''

        user = endpoints.get_current_user()
        return login.login(user)

    @endpoints.method(message_types.VoidMessage, CheckinResponseMessage, path='checkin',
                      http_method='POST', name='checkin')
    def checkin(self, request):
        '''A function which updates the Workday with the check in date. If the check in button
        is pressed in a valid time, the system updates the Workday entity with the date. If not, 
        the function returns an error, or raises an Issue if necessary.
        Needs - A valid date
        Returns - CheckinResponseMessage'''

        user = endpoints.get_current_user()

        querycheckin = Workday.query(Workday.employeeid == user.email(),
                                     Workday.date == datetime.datetime.now()).get()

        # querycheckin has the Workday of the employee in the proper day.
        if querycheckin.checkin is None:
            now = datetime.datetime.now()
            checkmin = now.replace(hour=7, minute=30, second=59, microsecond=0)
            checkmax = now.replace(hour=9, minute=00, second=59, microsecond=0)
            checkoutmax = now.replace(hour=19, minute=00, second=0, microsecond=0)

            if now < checkmin:
                # Error - Check in too soon
                return CheckinResponseMessage(response_code=400,
                                              text="You can't check in before 7:30 am")
            elif now >= checkoutmax:
                return CheckinResponseMessage(response_code=400,
                                              text="You can't check in after 19:00 pm")
            else:
                querycheckin.checkin = now
                querycheckin.put()
                if now < checkmax:
                    # Ok
                    return CheckinResponseMessage(response_code=200,
                                                  text="Successful Check in",
                                                  checkin=str(querycheckin.checkin))
                else:
                    # Issue - Check in too late.
                    return CheckinResponseMessage(response_code=200,
                                                  text="Check in out of time",
                                                  checkin=str(querycheckin.checkin))
        else:
            # Error - Check in after check in
            return CheckinResponseMessage(response_code=400, text="You can't check in again today")

    @endpoints.method(message_types.VoidMessage, CheckoutResponseMessage,
                      path='checkout', http_method='POST', name='checkout')
    def checkout(self, request):
        '''A function which updates the Workday with the checkout date and the total hours.
        If the checkout is made in a valid time, the system returns updates the Workday entity
        with the checkout date and total. If not, the system returns an error or raises an issue 
        if necessary'''
        user = endpoints.get_current_user()

        querycheckout = Workday.query(Workday.employeeid == user.email(),
                                      Workday.date == datetime.datetime.now()).get()

        if querycheckout.checkout is not None:
            # Error - Check out after check out
            return CheckoutResponseMessage(response_code=400,
                                           text="You can't check out if you checked out already")

        if querycheckout.checkin is None:
            # Error - Check out without check in
            return CheckoutResponseMessage(response_code=400,
                                           text="You can't check out without checking in")
        else:
            now = datetime.datetime.now()
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


app = endpoints.api_server([MainPage], restricted=False)
