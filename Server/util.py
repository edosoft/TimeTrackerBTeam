from functools import reduce
from models import Workday, User
from datetime import timedelta, datetime
from messages import WeekTotalMessage, CheckinResponseMessage


def get_week_total(user):

    first_date = datetime.now()

    start_date = first_date - timedelta(days=first_date.weekday())
    end_date = start_date + timedelta(days=6)

    # Query to return all workdays in a week by user
    requested_workdays = Workday.query(Workday.date >= start_date, Workday.date <= end_date)

    # From the list of workdays, get another list with each total
    week_hours = list(map((lambda day: day.total), requested_workdays))
    # Sums each daily total in the list to calc the week total
    week_total = reduce((lambda day_total, week_total: week_total + day_total), week_hours)

    return WeekTotalMessage(response_code=200,
                            user=user.email(),
                            hours=week_total)


def create_mock_user():
    # user = endpoints.get_current_user()
    workday_query = Workday.query(Workday.employee.email == "hrm@edosoft.es").get()

    if workday_query is None:
        auth = User(email="hrm@edosoft.es")
        auth.put()

        for day in range(1, 31):
            if day != 4 and day != 5 and day != 11 and day != 12 and day != 18 and day != 19 and day != 25 and day != 26:
                work = Workday()
                work.employee = auth
                work.date = datetime(2017, 11, day)
                work.checkin = datetime(2017, 11, day, 7, 31)
                work.checkout = datetime(2017, 11, day, 15, 2)
                work.total = 480
                work.put()

        return CheckinResponseMessage(response_code=200,
                                      text="Mock workdays created")

    return CheckinResponseMessage(response_code=200,
                                  text="Mock workdays returned")


def get_server_time():
    return datetime.now().time()