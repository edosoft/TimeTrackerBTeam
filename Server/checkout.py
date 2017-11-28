import datetime

from messages import CheckoutResponseMessage
from models import Workday


def checkout(user):
    '''A function which updates the Workday with the checkout date and the total hours.
    If the checkout is made in a valid time, the system returns updates the Workday entity
    with the checkout date and total. If not, the system returns an error or raises an issue 
    if necessary'''
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
        if now < checkmin:
            querycheckout.put()
            # Issue - Check out too soon
            return CheckoutResponseMessage(response_code=200,
                                           text="You checked out too early",
                                           checkout=str(querycheckout.checkout),
                                           total=querycheckout.total)
        else:
            if now > checknoon:  # If you go out after 15:00, a hour is substracted from the total
                querycheckout.total = querycheckout.total - 60

            if now < checkmax:
                querycheckout.put()
                # OK
                return CheckoutResponseMessage(response_code=200,
                                               text="Checkout Ok. Have a nice day :)",
                                               checkout=str(querycheckout.checkout),
                                               total=querycheckout.total)
            else:
                querycheckout.checkout = checkmax
                querycheckout.put()
                # Issue - Check out too late.
                return CheckoutResponseMessage(response_code=200,
                                               text="Check out out of time",
                                               checkout=str(querycheckout.checkout),
                                               total=querycheckout.total)