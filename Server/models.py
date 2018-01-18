from google.appengine.ext import ndb

# TODO: Insert User into Workday.


# [START Models]
class User(ndb.Model):
    """ Model to store an employee's valid login."""
    email = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty()
    admin = ndb.IntegerProperty()
    hrm = ndb.IntegerProperty()
    

class Workday(ndb.Model):
    """ Model to represent the workday of an employee."""
    employee = ndb.StructuredProperty(User)
    date = ndb.DateProperty(auto_now_add=True)
    checkin = ndb.DateTimeProperty(repeated=True)
    checkout = ndb.DateTimeProperty(repeated=True)
    ip_checkin = ndb.StringProperty(repeated=True)
    ip_checkout = ndb.StringProperty(repeated=True)
    total = ndb.IntegerProperty()

class Issue(ndb.Model):
    """ Model to represent an issue of an employee."""
    employee = ndb.StructuredProperty(User)
    date = ndb.DateTimeProperty()
    created = ndb.DateProperty()
    issue_type = ndb.StringProperty()
    non_viewed = ndb.IntegerProperty()
    non_solved = ndb.IntegerProperty()

    
# [END Models]
