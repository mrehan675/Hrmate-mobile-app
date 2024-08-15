# Copyright (c) 2024, rehan and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data","width": 120},
        {"label": "Log Type", "fieldname": "log_type", "fieldtype": "select", "options": "IN/OUT", "width": 120},
        {"label": "Address", "fieldname": "timeinaddress", "fieldtype": "Data","width": 120},
        {"label": "Time", "fieldname": "time", "fieldtype": "Datetime", "width": 120},
        {"label": "Attendance", "fieldname": "attendance", "fieldtype": "Link", "options": "Attendance", "width": 120},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        # {"label": "QTN Value", "fieldname": "total", "fieldtype": "Currency", "width": 100},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
        # {"label": "Profit QPS", "fieldname": "total_offered_price", "fieldtype": "Currency", "width": 100},
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += f" AND eck.posting_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND eck.posting_date <= '{filters['to_date']}'"
    if filters.get("Customer"):
        conditions += f" AND eck.Employee = '{filters['Employee']}'"
    if filters.get("Plant"):
        conditions += f" AND eck.company = '{filters['Company']}'"

    # def get_data(filters):
    # conditions = ""
    # if filters.get("from_date"):
    #     conditions += f" AND eck.time >= '{filters['from_date']}'"
    # if filters.get("to_date"):
    #     conditions += f" AND eck.time <= '{filters['to_date']}'"
    # Add conditions for other filters like Customer, Plant based on the fields available in "Employee Checkin" doctype

    query = f"""
        SELECT
            eck.employee,
            eck.employee_name,
            eck.log_type,
            eck.timeinaddress,
            eck.time,
            eck.attendance,
            eck.posting_date,
            eck.company
        FROM
            `tabEmployee Checkin` eck
        WHERE
            eck.docstatus = 0
            {conditions}
        ORDER BY
            eck.employee_name DESC
    """

    data = frappe.db.sql(query, as_dict=True)
    return data
