import frappe
from frappe import _

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
