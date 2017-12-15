import datetime

from messages import CheckinResponseMessage
from models import Workday


def check_in(user, current_date=None):
    """
    A function which updates the Workday with the check in date. If the check in button
    is pressed in a valid time, the system updates the Workday entity with the date. If not,
    the function returns an error, or raises an Issue if necessary.
    Needs - A valid date
    Returns - CheckinResponseMessage
    """
    if current_date is None:
        current_date = datetime.datetime.now()
        email = user.email()
    else:
        email = user.email

    check_in_query = Workday.query(Workday.employee.email == email,
                                   Workday.date == current_date).get()

    # check_in_query has the Workday of the employee in the proper day.
    if check_in_query.checkin is None:
        now = current_date
        check_in_min = now.replace(hour=7, minute=30, second=59, microsecond=0)
        check_in_max = now.replace(hour=9, minute=00, second=59, microsecond=0)
        check_out_max = now.replace(hour=19, minute=00, second=0, microsecond=0)

        # Error - Check in too soon
        if now < check_in_min:
            return CheckinResponseMessage(response_code=400,
                                          text="You can't check in before 7:30 am")
        elif now >= check_out_max:
            return CheckinResponseMessage(response_code=400,
                                          text="You can't check in after 19:00 pm")
        else:
            check_in_query.checkin = now
            check_in_query.put()

            # Ok
            if now < check_in_max:
                return CheckinResponseMessage(response_code=200,
                                              text="Successful Check in",
                                              checkin=str(check_in_query.checkin))

            # Issue - Check in too late.
            else:
                return CheckinResponseMessage(response_code=200,
                                              text="Check in out of time",
                                              checkin=str(check_in_query.checkin))

    # Error - Check in after check in
    else:
        return CheckinResponseMessage(response_code=400,
                                      checkin=str(check_in_query.checkin),
                                      text="You can't check in again today")
