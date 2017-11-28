#!/usr/bin/env python


from protorpc import messages
# Protocolo RPC.


class WeekReportMessage(messages.Message):
    email = messages.StringField(1)
    monday = messages.IntegerField(2)
    tuesday = messages.IntegerField(3)
    wednesday = messages.IntegerField(4)
    thursday = messages.IntegerField(5)
    friday = messages.IntegerField(6)
    total = messages.IntegerField(7)


class WeekResponseMessage(messages.Message):
    reports = messages.MessageField(WeekReportMessage, 1, repeated=True)
    response_code = messages.IntegerField(2, required=True)
    text = messages.StringField(3, required=True)


class WorkdayResponseMessage(messages.Message):
    response_code = messages.IntegerField(2, required=True)
    employeeid = messages.StringField(3)
    date = messages.StringField(4)
    checkin = messages.StringField(5)
    checkout = messages.StringField(6)
    total = messages.IntegerField(7)
    text = messages.StringField(1)


class CheckinResponseMessage(messages.Message):
    response_code = messages.IntegerField(2)
    text = messages.StringField(1)
    checkin = messages.StringField(3)


class CheckoutResponseMessage(messages.Message):
    response_code = messages.IntegerField(2)
    text = messages.StringField(1)
    checkout = messages.StringField(3)
    total = messages.IntegerField(4)