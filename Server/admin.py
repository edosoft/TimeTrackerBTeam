from models import User, Workday
from messages import ChangeRoleResponseMessage, RequestChangeRole
from messages import GetUserListResponseMessage, GetUserListMessage
from messages import IPUserMessage, IPUserResponseMessage, IPDateResponseMessage, IPDateMessage
from datetime import timedelta, datetime
def create_user():
    user_query_create = User.query(User.email == "admin@edosoft.es").get()
    if user_query_create is None:
        auth1 = User(email="hrm@edosoft.es", name="Helena Heras", admin = 0, hrm = 1)
        auth1.put()
        auth2 = User(email="admin@edosoft.es", name="Aitor Carrera", admin = 1, hrm = 1)
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
        auth8 = User(email="juan.vera@edosoft.es", name="Juan Vera", admin = 1, hrm = 1)
        auth8.put()
        auth9 = User(email="roberto.gonzalez@edosoft.es", name="Roberto Gonzalez", admin = 1, hrm = 1)
        auth9.put()
        auth10 = User(email="efren.perez@edosoft.es", name="Efren Perez", admin = 1, hrm = 1)
        auth10.put()
        auth11 = User(email="admin_m@edosoft.es", name="Antonio Arbelo", admin = 1, hrm = 0)
        auth11.put()


def get_user_list():
    user_query = User.query()

    if len(user_query.fetch()) < 1:
        return GetUserListResponseMessage(response_code=400, text="Error: Users not found")
    else:
        all_users = User.query().order(+User.name)
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
                                            text="User not found.")
    if type(hrm_value) is int and type(admin_value) is int:
        if user_query_change.email == user:
            if user_query_change.admin is not admin_value:
                return ChangeRoleResponseMessage(response_code=400, 
                                            text="You can not change your admin role.")
            else:
                user_query_change.hrm = hrm_value;
        else:
            user_query_change.admin = admin_value;
            user_query_change.hrm = hrm_value;
            
        user_query_change.put()
        return ChangeRoleResponseMessage(response_code=200, text="You have assigned the roles succesfully.")

    return ChangeRoleResponseMessage(response_code=400, 
                                            text="The values of roles are not correct.")
    
def get_ip_by_user(user_email, start_date, end_date):
    """
    A function which returns the IPs of a selected user and date. It returns the list
    of IPs, sorted by check in and checkout. 
    Needs - The date and user
    Returns - IPUserResponseMessage
    """
    first_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    last_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    requested_workdays = Workday.query(Workday.date >= first_date, Workday.date <= last_date)
    user = User.query(User.email == user_email).get()
    
    if user is None:
        return IPUserResponseMessage(response_code=400, text="User doesn't exist")
     
    else:
        result = []
        workdays_by_employee = requested_workdays.filter(
                Workday.employee.email == user_email).order(+Workday.date)

        for elem in workdays_by_employee:
            workday_ip_checkin = elem.ip_checkin
            workday_ip_checkout = elem.ip_checkout
            workday_date = str(elem.date)
            result.append(IPUserMessage(date=workday_date,
                                        ip_checkin=workday_ip_checkin,
                                        ip_checkout=workday_ip_checkout))
        
        #Create empty workdays if it's necessary.
        complete_workdays = []
        acc = 0
        for day in perdelta(first_date, last_date):
            query_find_day = workdays_by_employee.filter(Workday.date == day).get()
            if query_find_day is None:
                complete_workdays.append(IPUserMessage(date=str(day),
                                                       ip_checkin=[],
                                                       ip_checkout=[]))
            else:
                complete_workdays.append(result[acc])
                acc += 1

        result = complete_workdays
        return IPUserResponseMessage(response_code=200, text="Returning IP by User",
                                     ip_values=result, name=user.name)

def get_ip_by_date(selected_date):
    """
    A function which returns all the IPs of a selected date. It returns the list
    of IPs, sorted by check in and checkout. 
    Needs - The date
    Returns - IPUserResponseMessage
    """

    users = User.query()
    result = []
    for user in users:
        email = user.email
        raw_data_by_employee = get_ip_by_user(email, selected_date, selected_date)
        data_employee = IPDateMessage()
        data_employee.name = raw_data_by_employee.name
        data_employee.ip_checkin = raw_data_by_employee.ip_values[0].ip_checkin
        data_employee.ip_checkout = raw_data_by_employee.ip_values[0].ip_checkout
        result.append(data_employee)

    return IPDateResponseMessage(response_code=200, text="Returning IP by Date",
                                 ip_report=result)



def perdelta(start, end, delta=timedelta(days=1)):
    curr = start
    while curr <= end:
        yield curr
        curr += delta


