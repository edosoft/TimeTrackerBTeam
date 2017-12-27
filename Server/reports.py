from datetime import datetime, timedelta
import calendar

from messages import ReportMessage, ReportResponseMessage, WorkdayMessage
from models import User, Workday

def get_report(date, report_type=None):
    """
    A function which returns the reports of a selected date. It returns the user, 
    total hours per day and total hours in the range. 
    Needs - The date and last day to check
    Returns - ResponseMessage, an array of ReportMessages
    """

    # print(map(lambda x: x.date.isocalendar()[2], q))
    # AQUI

    if report_type == 1:
        first_date = datetime.strptime(date, "%Y-%m").date()
        cal = calendar.monthrange(first_date.year, first_date.month)
        start_date = first_date.replace(day=1)
        end_date = first_date.replace(day=cal[1])
    else:
        first_date = datetime.strptime(date + '-0', "%Y-W%W-%w").date()
        cal = calendar.monthrange(first_date.year, first_date.month)
        start_date = first_date - timedelta(days=first_date.weekday())
        end_date = start_date + timedelta(days=6)

    requested_workdays = Workday.query(Workday.date >= start_date, Workday.date <= end_date)

    if len(requested_workdays.fetch()) < 1:
        return ReportResponseMessage(response_code=400, text="There are no records in the selected date")

    else:
        all_users = User.query()
        result = []

        for user in all_users:
            employee_report = ReportMessage()
            total_hours_per_employee = []
            employee_report.email = user.email
            employee_report.name = user.name
            workdays_by_employee = requested_workdays.filter(
                Workday.employee.email == employee_report.email).order(+Workday.date)

            for elem in workdays_by_employee:
                workday_date = str(elem.date)
                day_of_week = elem.date.isocalendar()[2]
                employee_report.workday.append(WorkdayMessage(date=workday_date,
                                                              day_of_week=day_of_week,
                                                              total=elem.total))
                total_hours_per_employee.append(elem.total)

            #if report_type == 1:
                #employee_report.total_days_worked = len(workdays_by_employee.fetch())
            employee_report.total_days_worked = len(workdays_by_employee.fetch())
            employee_report.total = sum(total_hours_per_employee)
            
            #Create empty workdays if it's necessary.
            complete_workdays = []
            acc = 0
            for day in perdelta(start_date, end_date):
                query_find_day = workdays_by_employee.filter(Workday.date == day).get()
                if query_find_day is None:
                    complete_workdays.append(WorkdayMessage(date=str(day),
                                                            day_of_week=day.isocalendar()[2],
                                                            total=0))
                else:
                    complete_workdays.append(employee_report.workday[acc])
                    acc += 1
            employee_report.workday = complete_workdays
            #if len(workdays_by_employee.fetch()):
            #    result.append(employee_report)
            result.append(employee_report)
            
        return ReportResponseMessage(response_code=200, text="Returning report",
                                     reports=result, month=cal[1])


def perdelta(start, end, delta=timedelta(days=1)):
    curr = start
    while curr <= end:
        yield curr
        curr += delta