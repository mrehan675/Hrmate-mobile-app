import frappe
from frappe import auth
from frappe import local


@frappe.whitelist( allow_guest=True )
def login(usr, pwd):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key":0,
            "message":"Authentication Error!"
        }

        return

    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)
    token = frappe.get_doc('Mobile App Setting','Mobile App Setting')
    employee_list = get_employee_number(user.email)
    

    if employee_list:
        employee = employee_list[0]
        frappe.response["message"] = {
            "success_key":1,
            "message":"Authentication success",
            "sid":frappe.session.sid,
            "token":token.custom_token,
            "camera":token.is_camera,
            # "api_key":user.api_key,
            #  "api_secret":user.custom_api_secret,
            # "api_secret":api_generate,
            "username":user.username,
            "email":user.email,
            "role_type":user.role_type,
            "employee_no" : employee["name"],
            "company" : employee["company"],
            "leave_approver" : employee["leave_approver"],
        }
    else:
        frappe.response["message"] = {
            "success_key": 0,
            "message": "Employee not found"
        }

# def get_employee_number(user_email):
#     employee = frappe.get_list("Employee", filters={"user_id": user_email}, fields=["name","company"])
#     if employee:
#         return employee[0].get("name")
#     else:
#         return None
    
def get_employee_number(user_email):
    employee = frappe.get_list("Employee", filters={"user_id": user_email}, fields=["name","company","leave_approver"])
    if employee:
        return employee
    else:
            return None

def generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key

    user_details.api_secret = api_secret
    user_details.save()

    return api_secret

# @frappe.whitelist( allow_guest=True )
# def login(usr, pwd,url):
    
#     try:
#         login_manager = frappe.auth.LoginManager()
#         login_manager.authenticate(user=usr,pwd=pwd)
#         login_manager.post_login()
#         # Set the redirect URL
    
#         redirect_url = "https://rare-staging.srp.ai/app"
#         frappe.local.response["type"] = "redirect"
#         frappe.local.response["location"] = redirect_url

#     except frappe.exceptions.AuthenticationError:
#         frappe.clear_messages()
#         # Clear cache
#         frappe.clear_cache()
#         # frappe.local.response["message"] = {
#         #     "success_key":0,
#         #     "message":"Authentication Error!"
#         # }
#         # Set the redirect URL
    
#         redirect_url = "https://rare-staging.srp.ai/#login"
#         frappe.local.response["type"] = "redirect"
#         frappe.local.response["location"] = redirect_url


#         return

#     api_generate = generate_keys(frappe.session.user)
#     user = frappe.get_doc('User', frappe.session.user)

#     # frappe.response["message"] = {
#     #     "success_key":1,
#     #     "message":"Authentication success",
#     #     "sid":frappe.session.sid,
#     #     "api_key":user.api_key,
#     #     "api_secret":api_generate,
#     #     "username":user.username,
#     #     "email":user.email
#     # }
    


# def generate_keys(user):
#     user_details = frappe.get_doc('User', user)
#     api_secret = frappe.generate_hash(length=15)

#     if not user_details.api_key:
#         api_key = frappe.generate_hash(length=15)
#         user_details.api_key = api_key

#     user_details.api_secret = api_secret
#     user_details.save()

#     return api_secret

