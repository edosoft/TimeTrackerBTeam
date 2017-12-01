from datetime import datetime, timedelta
import calendar

from messages import ReportMessage, ReportResponseMessage, WorkdayMessage
from models import User, Workday

def get_report(date, isMonthly=None):
    '''A function which returns the reports of a selected date. It returns the user, 
    total hours per day and total hours in the range. 
    Needs - The date and last day to check
    Returns - ResponseMessage, an array of ReportMessages '''
    #print(map(lambda x: x.date.isocalendar()[2], q))
    #AQUI
    first_date = datetime.strptime(date, "%Y-%m-%d").date()
    cal = calendar.monthrange(first_date.year, first_date.month)
    if isMonthly == "True":
        start_date = first_date.replace(day=1)
        end_date = first_date.replace(day=cal[1])
    else:
        start_date = first_date - timedelta(days=first_date.weekday())
        end_date = start_date + timedelta(days=6)

    requested_workdays = Workday.query(Workday.date >= start_date, Workday.date <= end_date)

    if len(requested_workdays.fetch(10)) < 1:
        return ReportResponseMessage(response_code=400, text="There are no records in the selected date")
    else:
        all_users = User.query()
        result = []
        for user in all_users:
            report_employee = ReportMessage()
            total_hours_per_employee = []
            report_employee.email = user.email
            workdays_by_employee = requested_workdays.filter(
                Workday.employeeid == report_employee.email).order(+Workday.date)
            for elem in workdays_by_employee:
                date_workday = str(elem.date);
                day_week = elem.date.isocalendar()[2]
                report_employee.workday.append(WorkdayMessage(date = date_workday, day_week = day_week, total = elem.total))
                total_hours_per_employee.append(elem.total)

            if isMonthly == "True":
                report_employee.total_days_worked = len(workdays_by_employee.fetch())

            report_employee.total = sum(total_hours_per_employee)
            if len(workdays_by_employee.fetch()):
                result.append(report_employee)
        return ReportResponseMessage(response_code=200, text="Returning report", reports=result, month = cal[1])
