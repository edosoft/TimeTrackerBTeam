#!/usr/bin/env python
# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime

import endpoints

from google.appengine.ext import ndb
from protorpc import message_types
from protorpc import remote

from messages import LoginResponseMessage, WorkdayResponseMessage, \
CheckinResponseMessage, CheckoutResponseMessage


# [START greeting]
class User(ndb.Model):
    """Model to represent an employee's login."""
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
        '''A function who validates the login. It creater User and Workday entities '''
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

            querywork = Workday.query(Workday.employeeid == user.email(), \
            Workday.date == datetime.datetime.now()).get()

            if querywork is None:
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
                work = querywork
                return WorkdayResponseMessage(text = "Returning Workday", employeeid = work.employeeid, date = str(work.date), checkin = str(work.checkin),  checkout = str(work.checkout), total = work.total, response_code = 200)  


    @endpoints.method(message_types.VoidMessage, CheckinResponseMessage, path ='checkin', http_method='POST', name ='checkin')
    def checkin(self, request):
        user = endpoints.get_current_user()

        querywork = Workday.query(Workday.employeeid == user.email(), \
            Workday.date == datetime.datetime.now()).get()

        #Querywork has the Workday of the employee in the proper day.
        if querywork.checkin is None:
            querywork.checkin = datetime.datetime.now()
            querywork.put()
            return CheckinResponseMessage(response_code=200, text="Initializing Checkin")
        else:
            return CheckinResponseMessage(response_code=400, text="You can't check in again today")

    @endpoints.method(message_types.VoidMessage, CheckoutResponseMessage, \
    path='checkout', http_method='POST', name='checkout')
    def checkout(self, request):
        user = endpoints.get_current_user()

        querywork = Workday.query(Workday.employeeid == user.email(), \
            Workday.date == datetime.datetime.now()).get()

        #Querywork has the Workday of the employee in the proper day.
        if querywork.checkin is None:
            return CheckoutResponseMessage(response_code=400, \
        text="You can't check out without checking in")
        else:
            querywork.checkout = datetime.datetime.now()
            querywork.total = (querywork.checkout - querywork.checkin).seconds/3600
            querywork.put()
            return CheckoutResponseMessage(response_code=200, \
        text="Checkout Ok. Have a nice day :)")


app = endpoints.api_server([MainPage], restricted = False)