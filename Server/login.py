#!/usr/bin/env python


from protorpc import messages
#Protocolo RPC.

#user_id = messages.StringField(1, required=True)
#Cada vez que se agrega un campo nuevo, es necesario asignarle un integer para
#validar el protocolo RPC. Asi mismo se puede indicar si es un dato requerido, como se ve.
#Si esta requerido y no se envia, appEngine devuelve un error 400.
#Otro campo: repeated. Se vuelve un array, en este caso de StringFields.


class LoginResponseMessage(messages.Message):
    response_code = messages.IntegerField(1)
    email = messages.StringField(3)
    #email = messages.StringField(2)

