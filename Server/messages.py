#!/usr/bin/env python


from protorpc import messages
# Protocolo RPC.

# user_id = messages.StringField(1, required=True)
# Cada vez que se agrega un campo nuevo, es necesario asignarle un integer para
# validar el protocolo RPC. Asi mismo se puede indicar si es un dato requerido, como se ve.
# Si esta requerido y no se envia, appEngine devuelve un error 400.
# Otro campo: repeated. Se vuelve un array, en este caso de StringFields.


class LoginResponseMessage(messages.Message):
    response_code = messages.IntegerField(2, required=True)
    text = messages.StringField(1)
    # email = messages.StringField(2)


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