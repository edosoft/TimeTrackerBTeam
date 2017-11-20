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
import endpoints

from google.appengine.api.taskqueue import taskqueue
from google.appengine.ext import ndb
from protorpc import message_types
from protorpc import remote

from login import LoginResponseMessage

import os
import urllib
import json


# [START greeting]
class User(ndb.Model):
    """Sub model for representing an author."""
    email = ndb.StringProperty(indexed=True)



#v1 will be deprecated by Aug-2018, but it can be used for educational purposes
@endpoints.api(name='timetrackerApi', version='v1', allowed_client_ids=["953775827463-qnn5h5i227iaule8b9r575sgck494jbc.apps.googleusercontent.com"], scopes=[endpoints.EMAIL_SCOPE])
class MainPage(remote.Service):
    @endpoints.method(message_types.VoidMessage, LoginResponseMessage, path = 'login', http_method='POST',
                    name = 'login')
    def login(self, request):
        '''A function who validates the login '''
        # [START user_details]
        user = endpoints.get_current_user()
        #print (user.email())

        if user is None:
            return LoginResponseMessage(email="Error: Bag login", response_code=400)
        else:
            query = User.query(User.email == user.email()).get()
            if query is None:
                return LoginResponseMessage(email= "Not found in DB", response_code=300)
            else:
                #De aqui irias a checkin/checkout
                return LoginResponseMessage(email = user.email(), response_code = 200)
            
        #query = Author.query(user.user_id == request.user_id).get()
        # [END user_details]
        #return query
        #Si existe en la base de datos, lo devuelvo.
        #Si no, lo creo. 
        # [END main_page]


    @endpoints.method(message_types.VoidMessage, LoginResponseMessage, path = 'createUser', http_method='POST',
                    name = 'createUser')
    def createUser(self, request):
        user = endpoints.get_current_user()
        auth = User(email=user.email())
        auth.put()
        return LoginResponseMessage(email = user.email(), response_code = 200)

app = endpoints.api_server([MainPage], restricted = False)

'''
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
'''
