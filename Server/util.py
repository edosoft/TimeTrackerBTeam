from functools import reduce
from models import Workday
import datetime
from messages import WeekTotalMessage


def get_week_total(user):
    current_week = datetime.datetime.now().isocalendar()[1]

    # Query to return all workdays in a week by user
    query_week = Workday.query(Workday.employeeid == user.email(),
                               Workday.date.isocalendar()[1] == current_week).fetch()

    # From the list of workdays, get another list with each total
    week_hours = list(map((lambda day: day.total), query_week))
    # Sums each daily total in the list to calc the week total
    week_total = reduce((lambda day_total, week_total: week_total + day_total), week_hours)

    return WeekTotalMessage(response_code=200,
                            user=user.email,
                            hours=week_total)
