from models import User
from messages import ChangeRoleResponseMessage, RequestChangeRole
from messages import GetUserListResponseMessage, GetUserListMessage


def create_user():
    user_query_create = User.query(User.email == "admin@edosoft.es").get()

    if user_query_create is None:
        auth1 = User(email="hrm@edosoft.es", name="Helena Heras", admin = 0, hrm = 1)
        auth1.put()
        auth2 = User(email="admin@edosoft.es", name="Antonio Arbelo", admin = 1, hrm = 0)
        auth2.put()
        auth3 = User(email="javier.hernandez@edosoft.es", name="Javier Hernandez", admin = 1, hrm = 1)
        auth3.put()
        auth4 = User(email="luis.montero@edosoft.es", name="Luis Montero", admin = 1, hrm = 1)
        auth4.put()
        auth5 = User(email="maria.ramos@edosoft.es", name="Maria Ramos", admin = 1, hrm = 1)
        auth5.put()
        auth6 = User(email="nestor.marin@edosoft.es", name="Nestor Marin", admin = 1, hrm = 1)
        auth6.put()
        auth7 = User(email="deyan.guacaran@edosoft.es", name="Deyan Guacaran", admin = 1, hrm = 1)
        auth7.put()
        auth7 = User(email="empleado@edosoft.es", name="Paco Ramirez", admin = 0, hrm = 0)
        auth7.put()


def get_user_list():
    user_query = User.query()

    if len(user_query.fetch()) < 1:
        return GetUserListResponseMessage(response_code=400, text="Error: Users not found")
    else:
        all_users = User.query()
        result = []

        for user in all_users:
            user_information = GetUserListMessage()
            user_information.email=user.email
            user_information.name=user.name
            user_information.admin=user.admin
            user_information.hrm=user.hrm
            
            result.append(user_information)

        return GetUserListResponseMessage(response_code=200, text="Returning users list",
                                     user_list=result)            

def change_role(user_email, hrm_value, admin_value, user):
   
    user_query_change = User.query(User.email == user_email).get()

    if user_query_change is None:
        return ChangeRoleResponseMessage(response_code=400, 
                                            text="User not found")
    
    if type(hrm_value) is int and type(admin_value) is int:
        if user_query_change.email is user:
            print(user_query_change.admin)
            print(admin_value)
            if user_query_change.admin is not admin_value:
                return ChangeRoleResponseMessage(response_code=400, 
                                            text="Error: you can not change your admin role")
            else:
                user_query_change.hrm = hrm_value;
        else:
            user_query_change.admin = admin_value;
            user_query_change.hrm = hrm_value;
            
        user_query_change.put()
        return ChangeRoleResponseMessage(response_code=200, text="Correct change")

    return ChangeRoleResponseMessage(response_code=400, 
                                            text="The values of roles are not correct")

    
    