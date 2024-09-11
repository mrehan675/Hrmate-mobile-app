import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe.utils import nowdate
from datetime import datetime, timedelta





#Existing Api#
@frappe.whitelist()
def get_latest_checkins_status(employee, posting_date=None):
    if not posting_date:
        posting_date = nowdate()

    latest_checkin = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "employee": employee,
            "posting_date": posting_date
        },
        fields=["name", "log_type", "time", "posting_date"],
        order_by="time desc",
        limit=1
    )

     # Fetch the is_camera field from the Mobile Settings single DocType
    mobile_settings = frappe.get_single("Mobile App Setting")
    is_camera = mobile_settings.is_camera

    if latest_checkin:
        latest_checkin[0]["is_camera"] = is_camera
        return latest_checkin[0]
    else:
        return {
            "message": "No check-ins found for this employee on the given date",
            "is_camera": is_camera
        }





#New Api Method#
@frappe.whitelist()
def new_get_latest_checkins_status(employee, time=None):
    
    # Fetch the is_camera field from the Mobile Settings single DocType
    mobile_settings = frappe.get_single("Mobile App Setting")
    is_camera = mobile_settings.is_camera
    cycle_start = mobile_settings.cycle_start_time  # Assume it's "06:00:00"
    cycle_end = mobile_settings.cycle_end_time      # Assume it's "05:59:59"


    if not time:
        time = now_datetime()

    # Convert time to a datetime object if it's provided as a string
    if isinstance(time, str):
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    # Check if the time is before cycle_start (6:00 AM), if so, the day is considered as previous day
    posting_date = time.date()

    # If the current time is before the cycle start (6:00 AM), consider the previous day's cycle
    if time.time() < datetime.strptime(cycle_start, "%H:%M:%S").time():
        posting_date = posting_date - timedelta(days=1)

    # Start time is 6:00 AM of the posting_date
    start_time = datetime.combine(posting_date, datetime.strptime(cycle_start, "%H:%M:%S").time())

    # End time is 5:59 AM of the next day
    end_time = start_time + timedelta(days=1, seconds=-1)  # 5:59:59 of the next day

    # Fetch the latest check-in between the start_time and end_time
    latest_checkin = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "employee": employee,
            "time": ["between", [start_time, end_time]]
        },
        fields=["name", "log_type", "time", "posting_date"],
        order_by="time desc",
        limit=1
    )

    if latest_checkin:
        latest_checkin[0]["is_camera"] = is_camera
        return latest_checkin[0], start_time, end_time
    else:
        return {
            "message": "No check-ins found for this employee within the cycle time",
            "is_camera": is_camera
        }


@frappe.whitelist()
def up_new_get_latest_checkins_status(employee, time=None):
    # Fetch the is_camera field from the Mobile Settings single DocType
    mobile_settings = frappe.get_single("Mobile App Setting")
    is_camera = mobile_settings.is_camera
    cycle_start = mobile_settings.cycle_start_time  # Example: "06:00:00"
    cycle_end = mobile_settings.cycle_end_time      # Example: "05:59:59"

    if not time:
        time = now_datetime()

    # Convert time to a datetime object if it's provided as a string
    if isinstance(time, str):
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    # Get cycle start time for comparison
    cycle_start_time = datetime.strptime(cycle_start, "%H:%M:%S").time()

    # Determine the posting date based on whether the time is before or after 6:00 AM
    posting_date = time.date()

    if time.time() < cycle_start_time:
        # If time is before 6:00 AM, the cycle belongs to the previous day
        posting_date = posting_date - timedelta(days=1)

    # Start time is 6:00 AM of the posting_date
    start_time = datetime.combine(posting_date, cycle_start_time)

    # End time is 5:59 AM of the next day
    end_time = start_time + timedelta(days=1, seconds=-1)

    

    # Fetch the latest check-in between the current cycle's start_time and end_time
    latest_checkin = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "employee": employee,
            "time": ["between", [start_time, end_time]]
        },
        fields=["name", "log_type", "time", "posting_date"],
        order_by="time desc",
        limit=1
    )

    # # If a check-in is found within the current cycle, return it
    # if latest_checkin:
    #     # Ensure the check-in is part of the current cycle and not the previous day
    #     if latest_checkin[0]["time"] >= start_time and latest_checkin[0]["time"] <= end_time:
    #         latest_checkin[0]["is_camera"] = is_camera
    #         return latest_checkin[0], start_time, end_time
    #     else:
    #         # If the check-in is outside the current cycle (belongs to the previous day)
    #         return {
    #             "message": "No check-ins found for this employee in the current cycle",
    #             "is_camera": is_camera
    #         }
    # else:
    #     # If no check-in is found, return a message
    #     return {
    #         "message": "No check-ins found for this employee within the cycle time",
    #         "is_camera": is_camera
    #     }
    if latest_checkin:
        latest_checkin[0]["is_camera"] = is_camera
        return latest_checkin[0], start_time, end_time
    else:
        return {
            "message": "No check-ins found for this employee within the cycle time",
            "is_camera": is_camera
        }



@frappe.whitelist()
def get_employee_checkins_with_images(filters=None, limit_start=0, limit_page_length=10000):
    if filters:
        filters = frappe.parse_json(filters)
     
    # Define fixed fields
    fields = ["name", "employee_name", "timeinaddress", "log_type", "posting_date", "time", "company"]

    # Fetch Employee Checkin records based on filters
    employee_checkins = frappe.get_list(
        "Employee Checkin",
        filters=filters,
        fields=fields,
        limit_start=limit_start,
        limit_page_length=limit_page_length
    )
    
    # Initialize response
    response = []
    
    # Fetch attached image URL for each Employee Checkin record
    for checkin in employee_checkins:
        checkin_doc = frappe.get_doc("Employee Checkin", checkin["name"])
        image_url = None
        attached_image = frappe.get_all("File", filters={
            "attached_to_doctype": "Employee Checkin",
            "attached_to_name": checkin_doc.name,
            "attached_to_field": "image_test"  # Ensure this matches your field name
        }, fields=["file_url"])
        
        if attached_image:
            image_url = attached_image[0].get("file_url")
        
        # Add checkin data and image URL to the response
        checkin["image_url"] = image_url
        response.append(checkin)
    
    return response





def check_employee_checkins():
    try:
        print("rehan")
        # Get all employees
        employees = frappe.get_all("Employee", fields=["name", "employee_name"])
        current_date = now_datetime().date()

        for employee in employees:
            # if employee.name == "HR-EMP-00002":
            print("Employee check",employee.name)


            # Check if there is any "IN" check-in for today
            in_checkins = frappe.db.get_value(
                "Employee Checkin",
                {
                    "employee": employee.name,
                    "posting_date": current_date,
                    "log_type": "IN"
                },
                [ "time", "company"]
            )
            
            print("IN checkin",in_checkins)
            
            # Check if the last log is "IN"
            if in_checkins:
                print("enter in")
                
                check_out_exists = frappe.db.exists("Employee Checkin", {
                    "employee": employee.name,
                    "log_type": "OUT",
                    "posting_date": current_date
                })

                print("checout", check_out_exists)
                
                if not check_out_exists:
                    print("if not")
                    time_8pm = current_date.strftime("%Y-%m-%d") + " 20:00:00"

                    # Insert an "SYS OUT" log automatically
                    checkin_doc = frappe.get_doc({
                        "doctype": "Employee Checkin",
                        "employee": employee.name,
                        "employee_name": employee.employee_name,
                        "log_type": "SYS OUT",
                        "timeinaddress": "SYSTEM ADDED ADDRESS",
                        "time": time_8pm,
                        "company": in_checkins[1],
                        "posting_date": str(current_date)
                    })
                    
                    checkin_doc.insert() 
                    
                    frappe.db.commit()
            
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Employee Checkin Scheduler Error")

