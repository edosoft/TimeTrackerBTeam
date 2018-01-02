#!/usr/bin/env python

from protorpc import messages
from protorpc import message_types
class WorkdayMessage (messages.Message):
    date = messages.StringField(1)
    day_of_week = messages.IntegerField(2)
    total = messages.IntegerField(3)


class RequestReport(messages.Message):
    date = messages.StringField(1, required=True)
    report_type = messages.IntegerField(2)


class ReportMessage(messages.Message):
    email = messages.StringField(1)
    name = messages.StringField(5)
    workday = messages.MessageField(WorkdayMessage, 2, repeated=True)
    total = messages.IntegerField(3)
    total_days_worked = messages.IntegerField(4, required=False)


class ReportResponseMessage(messages.Message):
    reports = messages.MessageField(ReportMessage, 1, repeated=True)
    response_code = messages.IntegerField(2, required=True)
    text = messages.StringField(3, required=True)
    month = messages.IntegerField(4, required=False)


class GetUserListMessage(messages.Message):
    email = messages.StringField(1, required = True)
    name = messages.StringField(2, required = True)
    hrm = messages.IntegerField(3, required = True)
    admin = messages.IntegerField(4, required = True)

class GetUserListResponseMessage(messages.Message):
    user_list = messages.MessageField(GetUserListMessage, 1, repeated=True)
    response_code = messages.IntegerField(2, required=True)
    text = messages.StringField(3, required=True)


class RequestChangeRole(messages.Message):
    user_email = messages.StringField(1, required=True)
    hrm_value = messages.IntegerField(2, required=True)
    admin_value = messages.IntegerField(3, required=True)

class ChangeRoleResponseMessage(messages.Message):
    response_code = messages.IntegerField(1, required=True)
    text = messages.StringField(2, required=True)


class RequestCurrentDate(messages.Message):
    report_type = messages.IntegerField(2)


class CurrentDateResponseMessage(messages.Message):
    response_code = messages.IntegerField(2, required=True)
    text = messages.StringField(3, required=True)
    date = messages.StringField(4, required=True)

class WorkdayResponseMessage(messages.Message):
    response_code = messages.IntegerField(2)
    email = messages.StringField(3)
    date = messages.StringField(4)
    checkin = messages.StringField(5, repeated=True)
    checkout = messages.StringField(6, repeated=True)
    total = messages.IntegerField(7)
    text = messages.StringField(1)
    name = messages.StringField(8)
    hrm = messages.IntegerField(9)
    admin = messages.IntegerField(10)   

class CheckinResponseMessage(messages.Message):
    response_code = messages.IntegerField(2)
    text = messages.StringField(1)
    checkin = messages.StringField(3)
    number = messages.IntegerField(4)


class CheckoutResponseMessage(messages.Message):
    response_code = messages.IntegerField(2)
    text = messages.StringField(1)
    checkout = messages.StringField(3)
    total = messages.IntegerField(4)
    number = messages.IntegerField(5)


class WeekTotalMessage(messages.Message):
    response_code = messages.IntegerField(2)
    user = messages.StringField(1)
    minutes = messages.IntegerField(3)


class IssueMessage(messages.Message):
    employee = messages.StringField(1)
    date = messages.StringField(2)
    issue_type = messages.StringField(3)
    non_viewed = messages.IntegerField(4)
    non_solved = messages.IntegerField(5)


class IssuesPerEmployeeMessage(messages.Message):
    employee = messages.StringField(1)
    issues = messages.MessageField(IssueMessage, 2, repeated=True)
    total_unsolved_peremp = messages.IntegerField(3)
    total_unviewed_peremp = messages.IntegerField(4)


class IssueResponseMessage (messages.Message):
    issues_per_employee = messages.MessageField(IssuesPerEmployeeMessage, 1, repeated=True)
    response_code = messages.IntegerField(2)
    text = messages.StringField(3)
    total_unsolved = messages.IntegerField(4)
    total_unviewed = messages.IntegerField(5)