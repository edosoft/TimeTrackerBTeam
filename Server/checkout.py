from datetime import datetime, date
from messages import CheckoutResponseMessage
from models import Workday, Issue


def check_out(user, ip, current_date=None):
    """
    A function which updates the Workday with the checkout date and the total hours.
    If the checkout is made in a valid time, the system returns updates the Workday entity
    with the checkout date and total. If not, the system returns an error or raises an issue
    if necessary
    """

    if current_date is None:
        current_date = datetime.now()
        email = user.email()
    else:
        email = user.email

    check_out_query = Workday.query(Workday.employee.email == email,
                                    Workday.date == current_date).get()

    # Error - Check out without a check in
    if len(check_out_query.checkout) > 2:
        return CheckoutResponseMessage(response_code=400,
                                       text="You can't check out more than 3 times")

    # Error - As many checks out as checks in
    if len(check_out_query.checkout) is len(check_out_query.checkin):
        return CheckoutResponseMessage(response_code=400,
                                       text="You can't check out without checking in")

    else:
        time_difference = current_date - check_out_query.checkin[-1]
        check_out_minus_check_in = time_difference.seconds / 60
        #CAMBIAR LUEGO
        if check_out_minus_check_in < 5:
            return CheckoutResponseMessage(response_code=300,
                                           text="You can't check out until 5 minutes have passed")



        now = current_date
        check_out_min = now.replace(hour=14, minute=00, second=0, microsecond=0)
        check_out_max = now.replace(hour=19, minute=00, second=0, microsecond=0)
        #lunch_time = now.replace(hour=15, minute=00, second=0, microsecond=0)

        check_out_query.checkout.append(now)
        check_out_query.ip_checkout.append(ip)
        check_out_query.total = check_out_query.total + check_out_minus_check_in

        # Issue - Check out too soon
        if now < check_out_min:
            check_out_query.put()
            issue = Issue.query(Issue.issue_type == "Early Check Out", Issue.employee == check_out_query.employee, Issue.created == current_date.date()).get() 
            if issue is None:
                issue = Issue()    
                issue.employee = check_out_query.employee
                issue.date = check_out_query.checkout[-1]
                issue.issue_type = "Early Check Out"
                issue.created = current_date.date()
                issue.non_viewed = 1
                issue.non_solved = 1
                issue.put()
                
            else:
                issue.date = check_out_query.checkout[-1]
                issue.put()

            return CheckoutResponseMessage(response_code=200,
                                           text="You checked out too early",
                                           checkout=str(check_out_query.checkout[-1]),
                                           number=len(check_out_query.checkout),
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
                                               text="Successful Check out",
                                               checkout=str(check_out_query.checkout[-1]),
                                               number=len(check_out_query.checkout),
                                               total=check_out_query.total)

            # Issue - Check out too late
            else:
                check_out_query.checkout[-1] = check_out_max
                check_out_query.put()
                issue = Issue()
                issue.employee = check_out_query.employee
                issue.issue_type = "Automatic Check Out"
                issue.non_viewed = 1
                issue.non_solved = 1
                issue.put()
                return CheckoutResponseMessage(response_code=200,
                                               text="Check out out of time",
                                               checkout=str(check_out_query.checkout[-1]),
                                               number=len(check_out_query.checkout),
                                               total=check_out_query.total)
