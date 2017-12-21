import datetime

from messages import WorkdayResponseMessage
from models import User, Workday


def log_in(user, current_date=None):
    """
    A function which validates the login. It creates a new User if it doesn't exist in the DB,
    and new Workday entities if the valid user hasn't logged in that day. If it's a returning user,
    this function returns the created Workday.
    Needs - User verified by Google.
    Returns - WorkdayResponseMessage.
    """

    # Error - Logging without authenticating with Google
    if user is None:
        return WorkdayResponseMessage(text="Error: Invalid Data", response_code=400)

    else:
        '''
        verify_email = user.email().split('@')[1]
        if (verify_email != 'edosoft.es'):
            return WorkdayResponseMessage(text="Error: Invalid Domain", response_code=400)
        '''
        if current_date is None:
            current_date = datetime.datetime.now()
            email = user.email()
        else:
            email = user.email
        


        user_query = User.query(User.email == email).get()

        # If the user doesn't exist, it inserts it to the database.
        if user_query is None:
            auth = User(email=email)
            auth.put()

        workday_query = Workday.query(Workday.employee == User(email=email),
                                      Workday.date == current_date).get()

        # If there is no workday, a new one is created and added to the DB.
        if workday_query is None:
            work = Workday()
            work.employee = User(email=email)
            work.checkin = []
            work.checkout = []
            work.total = 0
            work.put()
            return WorkdayResponseMessage(text="Creating Workday", employee=work.employee.email,
                                          date=str(work.date), checkin=work.checkin,
                                          checkout=work.checkout, total=work.total,
                                          response_code=200)

        # Ok - Returning existent
        else:
            work = workday_query
            strcin = []
            strcout = []
            for cin in work.checkin:
                strcin.append(str(cin))
            for cout in work.checkout:
                strcout.append(str(cout))
            
            return WorkdayResponseMessage(text="Returning Workday", employee=work.employee.email,
                                          date=str(work.date), checkin=strcin,
                                          checkout=strcout, total=work.total,
                                          response_code=200)
