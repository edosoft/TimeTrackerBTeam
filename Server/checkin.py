import datetime

from messages import CheckinResponseMessage
from models import Workday


def checkin(user):
    '''A function which updates the Workday with the check in date. If the check in button
    is pressed in a valid time, the system updates the Workday entity with the date. If not, 
    the function returns an error, or raises an Issue if necessary.
    Needs - A valid date
    Returns - CheckinResponseMessage'''

    querycheckin = Workday.query(Workday.employee.email == user.email(),
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
        return CheckinResponseMessage(response_code=400,
                                      checkin=str(querycheckin.checkin),
                                      text="You can't check in again today")
