#!/usr/bin/env python

import datetime

import endpoints

from google.appengine.ext import ndb
from protorpc import message_types
from protorpc import remote

from messages import WorkdayResponseMessage, CheckinResponseMessage, CheckoutResponseMessage


# [START Models]
class User(ndb.Model):
    """Model to store an employee's valid login."""
    email = ndb.StringProperty(indexed=True)


class Workday(ndb.Model):
    """ Model to represent the workday of an employee."""
    employeeid = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)
    checkin = ndb.DateTimeProperty()
    checkout = ndb.DateTimeProperty()
    total = ndb.IntegerProperty()

# [END Models]
# v1 will be deprecated by Aug-2018, but it can be used for educational purposes


@endpoints.api(name='timetrackerApi', version='v1',
               allowed_client_ids=["368116371345-ott8mvobq0aqcd8dvpu40b5n2fdjgs8v.apps.googleusercontent.com"],
               scopes=[endpoints.EMAIL_SCOPE])
class MainPage(remote.Service):

    @endpoints.method(message_types.VoidMessage, WorkdayResponseMessage, path='login',
                      http_method='POST', name='login')
    def login(self, request):
        '''A function which validates the login. It creates User and Workday entities '''
        user = endpoints.get_current_user()

        if user is None:
            # Error - Logging without authenticating with Google
            return WorkdayResponseMessage(text="Error: Invalid Data", response_code=400)
        else:
            query = User.query(User.email == user.email()).get()
            # If the user doesn't exist, it inserts it to the database.
            if query is None:
                auth = User(email=user.email())
                auth.put()

            queryworkday = Workday.query(Workday.employeeid == user.email(),
                                         Workday.date == datetime.datetime.now()).get()

            if queryworkday is None:
                # If there is no workday, a new one is created and added to the DB.
                work = Workday()
                work.employeeid = user.email()
                work.checkin = None
                work.checkout = None
                work.total = 0
                work.put()

                # Ok - Creating workday
                return WorkdayResponseMessage(text="Creating Workday", employeeid=work.employeeid,
                                              date=str(work.date), checkin=str(work.checkin),
                                              checkout=str(work.checkout), total=work.total,
                                              response_code=200)
            else:
                work = queryworkday

                str_checkin = "%s:%s" % (work.checkin.hour, work.checkin.minute)
                str_checkout = "%s:%s" % (work.checkout.hour, work.checkout.minute)


                # Ok - Returning existent
                return WorkdayResponseMessage(text="Returning Workday", employeeid=work.employeeid,
                                              date=str(work.date), checkin=str_checkin,
                                              checkout=str_checkout, total=work.total,
                                              response_code=200)

    @endpoints.method(message_types.VoidMessage, CheckinResponseMessage, path='checkin',
                      http_method='POST', name='checkin')
    def checkin(self, request):
        '''A function which updates the Workday with the check in date'''
        user = endpoints.get_current_user()

        querycheckin = Workday.query(Workday.employeeid == user.email(),
                                     Workday.date == datetime.datetime.now()).get()

        # querycheckin has the Workday of the employee in the proper day.
        if querycheckin.checkin is None:
            now = datetime.datetime.now()
            checkmin = now.replace(hour=7, minute=30, second=59, microsecond=0)
            checkmax = now.replace(hour=9, minute=00, second=59, microsecond=0)

            if now < checkmin:
                # Error - Check in too soon
                return CheckinResponseMessage(response_code=400,
                                              text="You can't check in before 7:30 am")
            else:
                querycheckin.checkin = now
                querycheckin.put()
                str_checkin = "%s:%s" % (querycheckin.checkin.hour, querycheckin.checkin.minute)
                if now < checkmax:
                    # Ok
                    return CheckinResponseMessage(response_code=200,
                                                  text="Successful Check in",
                                                  checkin=str_checkin)
                else:
                    # Issue - Check in too late.
                    return CheckinResponseMessage(response_code=200,
                                                  text="Check in out of time",
                                                  checkin=str_checkin)
        else:
            # Error - Check in after check in
            return CheckinResponseMessage(response_code=400, text="You can't check in again today")

    @endpoints.method(message_types.VoidMessage, CheckoutResponseMessage,
                      path='checkout', http_method='POST', name='checkout')
    def checkout(self, request):
        '''A function which updates the Workday with the check out date and the total hours'''
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
            str_checkout = "%s:%s" % (querycheckout.checkout.hour, querycheckout.checkout.minute)
            if now < checkmin:
                querycheckout.put()
                # Issue - Check out too soon
                return CheckoutResponseMessage(response_code=200,
                                               text="You checked out too early",
                                               checkout=str_checkout,
                                               total=querycheckout.total)
            else:
                if now > checknoon:  # If you go out after 15:00, a hour is substracted from the total
                    querycheckout.total = querycheckout.total - 60

                if now < checkmax:
                    querycheckout.put()
                    # OK
                    return CheckoutResponseMessage(response_code=200,
                                                   text="Checkout Ok. Have a nice day :)",
                                                   checkout=str_checkout,
                                                   total=querycheckout.total)
                else:
                    querycheckout.checkout = checkmax
                    querycheckout.put()
                    str_checkout = "%s:%s" % (querycheckout.checkout.hour, querycheckout.checkout.minute)
                    # Issue - Check out too late.
                    return CheckoutResponseMessage(response_code=200,
                                                   text="Check out out of time",
                                                   checkout=str_checkout,
                                                   total=querycheckout.total)


app = endpoints.api_server([MainPage], restricted=False)
