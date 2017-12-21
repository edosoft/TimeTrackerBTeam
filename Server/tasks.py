import datetime
from models import Workday


# Helper for the queued task to close all pending checkouts
def automatic_checkout_helper():

    # Returns today's workdays
    workday_query = Workday.query(Workday.date == datetime.date.today()).fetch()

    # Updates checkout for each workday
    for workday in workday_query:
        if len(workday.checkin) is not len(workday.checkout):
            workday.checkout.append(datetime.datetime.now())
            workday.put()
