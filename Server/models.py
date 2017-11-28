from google.appengine.ext import ndb

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
