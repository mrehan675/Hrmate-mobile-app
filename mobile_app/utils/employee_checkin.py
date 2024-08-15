import frappe
from frappe import _
from frappe.utils import now_datetime





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
        # Get all employees
        employees = frappe.get_all("Employee", fields=["name", "employee_name"])

        for employee in employees:
            # Get the latest check-in log for the employee
            last_checkin = frappe.db.get_value("Employee Checkin", 
                                               {"employee": employee.name}, 
                                               ["log_type", "time"], 
                                               order_by="time desc")
            
            # Check if the last log is "IN"
            if last_checkin and last_checkin[0] == "IN":
                # Check if an "OUT" log is missing for the day
                current_date = now_datetime().date()
                check_out_exists = frappe.db.exists("Employee Checkin", {
                    "employee": employee.name,
                    "log_type": "OUT",
                    "time": ["between", [str(current_date) + " 00:00:00", str(current_date) + " 23:59:59"]]
                })
                
                if not check_out_exists:
                    # Insert an "OUT" log automatically
                    checkin_doc = frappe.get_doc({
                        "doctype": "Employee Checkin",
                        "employee": employee.name,
                        "employee_name": employee.employee_name,
                        "log_type": "SYS OUT",
                        "time": now_datetime()
                    })
                    checkin_doc.insert()
                    frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Employee Checkin Scheduler Error")

