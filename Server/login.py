import datetime

from messages import WorkdayResponseMessage
from models import User, Workday


def login(user):
    '''A function which validates the login. It creates a new User if it doesn't exist in the DB,
     and new Workday entities if the valid user hasn't logged in that day. If it's a returning user,
     this function returns the created Workday.
     Needs - User verified by Google.
     Returns - WorkdayResponseMessage. '''

    if user is None:
        # Error - Logging without authenticating with Google
        return WorkdayResponseMessage(text="Error: Invalid Data", response_code=400)
    else:

        query = User.query(User.email == user.email()).get()
        # If the user doesn't exist, it inserts it to the database.
        if query is None:
            auth = User(email=user.email())
            auth.put()

        queryworkday = Workday.query(Workday.employee == User(email=user.email()),
                                     Workday.date == datetime.datetime.now()).get()

        if queryworkday is None:
            # If there is no workday, a new one is created and added to the DB.
            work = Workday()
            work.employee = User(email=user.email())
            work.checkin = None
            work.checkout = None
            work.total = 0
            work.put()


            # Ok - Creating workday
            return WorkdayResponseMessage(text="Creating Workday", employee=work.employee.email,
                                          date=str(work.date), checkin=str(work.checkin),
                                          checkout=str(work.checkout), total=work.total,
                                          response_code=200)
        else:
            work = queryworkday
            # Ok - Returning existent
            return WorkdayResponseMessage(text="Returning Workday", employee=work.employee.email,
                                          date=str(work.date), checkin=str(work.checkin),
                                          checkout=str(work.checkout), total=work.total,
                                          response_code=200)
