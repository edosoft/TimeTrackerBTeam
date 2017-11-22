#!/usr/bin/env python

import datetime

import endpoints

from google.appengine.ext import ndb
from protorpc import message_types
from protorpc import remote

from messages import LoginResponseMessage, WorkdayResponseMessage, \
CheckinResponseMessage, CheckoutResponseMessage


# [START greeting]
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

#v1 will be deprecated by Aug-2018, but it can be used for educational purposes

@endpoints.api(name='timetrackerApi', version='v1', \
allowed_client_ids=["368116371345-ott8mvobq0aqcd8dvpu40b5n2fdjgs8v.apps.googleusercontent.com"], \
scopes=[endpoints.EMAIL_SCOPE])

class MainPage(remote.Service):
    @endpoints.method(message_types.VoidMessage, WorkdayResponseMessage, path='login', \
    http_method='POST', name='login')
    def login(self, request):
        '''A function which validates the login. It creates User and Workday entities '''
        user = endpoints.get_current_user()

        if user is None:
            #If you try to sign in without succesfully loggin in:
            return WorkdayResponseMessage(text="Error: Invalid Data", response_code=400)
        else:
            query = User.query(User.email == user.email()).get()
            #If the user doesn't exist, it inserts it to the database.
            if query is None:
                auth = User(email=user.email())
                auth.put()

            queryworkday = Workday.query(Workday.employeeid == user.email(), \
            Workday.date == datetime.datetime.now()).get()

            if queryworkday is None:
                #If there is no workday, a new one is created and added to the DB.
                work = Workday()
                work.employeeid = user.email()
                work.checkin = None
                work.checkout = None
                work.total = 0
                work.put()
                return WorkdayResponseMessage(text="Creating Workday", employeeid=work.employeeid, \
                date=str(work.date), checkin=str(work.checkin), checkout=str(work.checkout), \
                total=work.total, response_code=200)
            else:
                work = queryworkday
                #If it exists, it is returned.
                return WorkdayResponseMessage(text = "Returning Workday", employeeid = work.employeeid, date = str(work.date), checkin = str(work.checkin),  checkout = str(work.checkout), total = work.total, response_code = 200)  


    @endpoints.method(message_types.VoidMessage, CheckinResponseMessage, path ='checkin', http_method='POST', name ='checkin')
    def checkin(self, request):
        '''A function which updates the Workday with the check in date'''
        user = endpoints.get_current_user()

        querycheckin = Workday.query(Workday.employeeid == user.email(), \
            Workday.date == datetime.datetime.now()).get()

        #querycheckin has the Workday of the employee in the proper day.
        if querycheckin.checkin is None:
            querycheckin.checkin = datetime.datetime.now()
            querycheckin.put()
            return CheckinResponseMessage(response_code=200, text="Initializing Check in")
        else:
            return CheckinResponseMessage(response_code=400, text="You can't check in again today")

    @endpoints.method(message_types.VoidMessage, CheckoutResponseMessage, \
    path='checkout', http_method='POST', name='checkout')
    def checkout(self, request):
        '''A function which updates the Workday with the check out date and the total hours'''
        user = endpoints.get_current_user()

        querycheckout = Workday.query(Workday.employeeid == user.email(), \
            Workday.date == datetime.datetime.now()).get()

        #Querywork has the Workday of the employee in the proper day.
        if querycheckout.checkin is None:
            return CheckoutResponseMessage(response_code=400, \
        text="You can't check out without checking in")
        else:
            querycheckout.checkout = datetime.datetime.now()
            querycheckout.total = (querycheckout.checkout - querycheckout.checkin).seconds/3600
            querycheckout.put()
            return CheckoutResponseMessage(response_code=200, \
        text="Checkout Ok. Have a nice day :)")


app = endpoints.api_server([MainPage], restricted = False)