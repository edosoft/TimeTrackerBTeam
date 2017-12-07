import datetime

from messages import CheckoutResponseMessage
from models import Workday


def check_out(user):
    """
    A function which updates the Workday with the checkout date and the total hours.
    If the checkout is made in a valid time, the system returns updates the Workday entity
    with the checkout date and total. If not, the system returns an error or raises an issue
    if necessary
    """

    check_out_query = Workday.query(Workday.employee.email == user.email(),
                                    Workday.date == datetime.datetime.now()).get()

    # Error - Check out after check out
    if check_out_query.checkout is not None:
        return CheckoutResponseMessage(response_code=400, checkout=str(check_out_query.checkout),
                                       text="You can't check out if you checked out already")

    # Error - Check out without check in
    if check_out_query.checkin is None:
        return CheckoutResponseMessage(response_code=400,
                                       text="You can't check out without checking in")

    else:
        now = datetime.datetime.now()
        check_out_min = now.replace(hour=14, minute=00, second=0, microsecond=0)
        check_out_max = now.replace(hour=19, minute=00, second=0, microsecond=0)
        #lunch_time = now.replace(hour=15, minute=00, second=0, microsecond=0)

        check_out_query.checkout = datetime.datetime.now()
        check_out_query.total = (check_out_query.checkout - check_out_query.checkin).seconds / 60

        # Issue - Check out too soon
        if now < check_out_min:
            check_out_query.put()
            return CheckoutResponseMessage(response_code=200,
                                           text="You checked out too early",
                                           checkout=str(check_out_query.checkout),
                                           total=check_out_query.total)

        else:
            # If you go out after 15:00, a hour is substracted from the total
            # TO LOOK. This doesn't work if you check in veeeery late.
            '''
            if now > lunch_time:
                check_out_query.total = check_out_query.total - 60
            '''
            # OK
            if now < check_out_max:
                check_out_query.put()
                return CheckoutResponseMessage(response_code=200,
                                               text="Checkout Ok. Have a nice day :)",
                                               checkout=str(check_out_query.checkout),
                                               total=check_out_query.total)

            # Issue - Check out too late
            else:
                check_out_query.checkout = check_out_max
                check_out_query.put()
                return CheckoutResponseMessage(response_code=200,
                                               text="Check out out of time",
                                               checkout=str(check_out_query.checkout),
                                               total=check_out_query.total)
