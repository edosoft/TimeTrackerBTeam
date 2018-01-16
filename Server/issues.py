from messages import GetUserListMessage, IssueResponseMessage, IssueMessage, IssuesPerEmployeeMessage, WorkdayIssueMessage, WorkdayIssueResponseMessage, IssueCorrectionResponseMessage
from models import User, Workday, Issue


def get_user_with_issues():
    """
    A function which returns an array of employees with issues, every employee is also an
    array who contains all the issues that had been generated returning in case of a positive
    search, a: response code: 200, text: returning issues, issues_per_employee who contains
    every employee's issue, and the total non viewed and non resolved, in case that there
    aren't employees with issues the return is a response code of 200 and a text: There
    aren't users with issues
    """
    all_issues = Issue.query().fetch()
    request_users = User.query().fetch()

    if (len(all_issues) < 1):
        return IssueResponseMessage(response_code=200, text='There aren`t users with issues')
    else:
        result = []
        total_issues_nonviewed = []
        total_issues_nonsolved = []

        for user in request_users:

            new_employee = IssuesPerEmployeeMessage()
            new_employee.employee = user.name
            total_issues_nonviewed_peremp = []
            total_issues_nonsolved_peremp = []

            request_issues = Issue.query(
                Issue.employee.email == user.email).fetch()

            for issue in request_issues:

                new_issue = IssueMessage()
                new_issue.date = str(issue.date)
                new_issue.issue_type = issue.issue_type
                new_issue.non_viewed = issue.non_viewed
                new_issue.non_solved = issue.non_viewed
                total_issues_nonsolved.append(issue.non_solved)
                total_issues_nonviewed.append(issue.non_viewed)
                total_issues_nonsolved_peremp.append(issue.non_solved)
                total_issues_nonviewed_peremp.append(issue.non_viewed)
                new_employee.issues.append(new_issue)

            new_employee.total_unsolved_peremp = sum(
                total_issues_nonsolved_peremp)
            new_employee.total_unviewed_peremp = sum(
                total_issues_nonviewed_peremp)
            if len(request_issues) is not 0:
                result.append(new_employee)

        total_unsolved = sum(total_issues_nonsolved)
        total_unviewed = sum(total_issues_nonviewed)

        return IssueResponseMessage(
            response_code=200, text='Returning Issues',
                                    issues_per_employee=result,
                                    total_unsolved=total_unsolved,
                                    total_unviewed=total_unviewed)


def get_workday_from_issues(email, date):
    user = User.query(User.email == email).get()
    if user is not None:
        wissue = Issue.query(
            Issue.employee == user, Issue.created == date).get()
        if wissue is not None:
            wissue.non_viewed = 0
            wissue.put()
            wday = Workday.query(
                Workday.employee == user, Workday.date == date).get()
            workday = WorkdayIssueMessage()
            employee = GetUserListMessage()
            employee.email = wday.employee.email
            employee.name = wday.employee.name
            employee.admin = wday.employee.admin
            employee.hrm = wday.employee.hrm

            workday.employee = employee
            strcin = []
            strcout = []
            for cin in wday.checkin:
                strcin.append(str(cin))
            for cout in wday.checkout:
                strcout.append(str(cout))
            workday.checkin = strcin
            workday.checkout = strcout
            return WorkdayIssueResponseMessage(response_code=200, workday=workday)
        else:
            return WorkdayIssueResponseMessage(response_code=400, text='No issue found')
    else:
        return WorkdayIssueResponseMessage(response_code=400, text='No user found')


def correct_issue(email, date, issue_type, correction):
    corrected = False
    user = User.query(User.email == email).get()
    if user is not None:
        issue = Issue.query(
            Issue.employee == user, Issue.created == date, Issue.issue_type == issue_type).get()
        if issue is not None:
            issue_workday = Workday.query(
                Workday.employee == user, Workday.date == date).get()

            if issue_type == 'Late Check In':
                issue_workday.checkin = correction
                corrected = True
            if issue_type == 'Early Check Out' or issue_type == 'Automatic Check Out':
                issue_workday.checkout = correction
                corrected = True

            if corrected is True:
                issue.non_solved = 0
                issue.put()
                issue_workday.put()
                return IssueCorrectionResponseMessage(response_code=200, text='Issue corrected')
            else:
                return IssueCorrectionResponseMessage(response_code=400, text='Issue not corrected')
        else:
            return IssueCorrectionResponseMessage(response_code=400, text='No issue found')
    else:
        return IssueCorrectionResponseMessage(response_code=400, text='No user found')
