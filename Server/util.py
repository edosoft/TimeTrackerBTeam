from functools import reduce
from models import Workday, User
from datetime import timedelta, datetime, date
from messages import WeekTotalMessage, CheckinResponseMessage
from messages import CurrentDateResponseMessage, RequestCurrentDate


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


def current_date(report_type):

    year = datetime.now()
    year = str(year.isocalendar()[0])

    if report_type is 0:
        week = datetime.now()
        week = str(week.isocalendar()[1]) 
        week_calendar = str(year + '-W' + week) #return the current week with this format: YYYY-WW
        return CurrentDateResponseMessage(response_code=200, text="Saved initial week for the calendar",date=week_calendar)

    else: 
        month = datetime.now()
        month = str(month.month) 
        month_calendar = str(year + '-' + month) #return the current week with this format: YYYY-MM
        return CurrentDateResponseMessage(response_code=200, text="Saved initial week for the calendar", date=month_calendar)

def create_mock_user():
    # user = endpoints.get_current_user()
    workday_query = Workday.query(Workday.employee.email == "hrm@edosoft.es").get()

    if workday_query is None:   #Workdays for all users are created.
        users = User.query()

        for user_w in users:
            '''
            for day in range(1, 31):
                first_date = date(2017, 11, day)
                
                day_of_week = first_date.isocalendar()[2]

                if day_of_week is not 6 and day_of_week is not 7:
                    work = Workday()
                    cin = []
                    cout = []
                    work.employee = user_w
                    work.date = datetime(2017, 11, day)
                    cin.append(datetime(2017, 11, day, 7, 31))
                    work.checkin = cin
                    cout.append(datetime(2017, 11, day, 15, 2))
                    work.checkout = cout
                    work.total = 480
                    work.put()
            '''
            for day in range(1, 26):
                    first_date = date(2017, 12, day)
                    
                    day_of_week = first_date.isocalendar()[2]

                    if day_of_week is not 6 and day_of_week is not 7:
                        work = Workday()
                        cin = []
                        cout = []
                        work.employee = user_w
                        work.date = datetime(2017, 12, day)
                        cin.append(datetime(2017, 12, day, 7, 31))
                        work.checkin = cin
                        cout.append(datetime(2017, 12, day, 15, 2))
                        work.checkout = cout
                        work.total = 480
                        work.put()

    else:
        #Mock different values to show
        date_bad = date(2017, 12, 20)
        date_exc = date(2017, 12, 14)
        workday_n_bad = Workday.query(Workday.employee.email == "nestor.marin@edosoft.es",
                                  Workday.date == date_bad).get()
        workday_n_bad.total = 420
        workday_n_bad.put()

        workday_n_exc = Workday.query(Workday.employee.email == "nestor.marin@edosoft.es",
                                  Workday.date == date_exc).get()
        workday_n_exc.total = 547
        workday_n_exc.put()           
        return CheckinResponseMessage(response_code=200,
                                      text="Mock workdays created")

    return CheckinResponseMessage(response_code=200,
                                  text="Mock workdays returned")

