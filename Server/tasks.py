import datetime
from models import Workday


# Helper for the queued task to close all pending checkouts
def automatic_checkout_helper():

    # Returns today's workdays
    queryWorkday = Workday.query(Workday.date == datetime.date.today()).fetch()

    # Updates checkout for each workday
    for workday in queryWorkday:
        if workday.checkin is not None and workday.checkout is None:
            workday.checkout = datetime.datetime.now()
            workday.put()
