import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe.utils import nowdate

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

