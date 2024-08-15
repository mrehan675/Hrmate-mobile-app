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
        # {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 140},
        {"label": "(IN)", "fieldname": "log_type_in", "fieldtype": "Data", "width": 60},
        {"label": "Address (IN)", "fieldname": "address_in", "fieldtype": "Data", "width": 240},
        {"label": "Time (IN)", "fieldname": "time_in", "fieldtype": "Datetime", "width": 160},
        {"label": "(OUT)", "fieldname": "log_type_out", "fieldtype": "Data", "width": 70},
        {"label": "Address (OUT)", "fieldname": "address_out", "fieldtype": "Data", "width": 240},
        {"label": "Time (OUT)", "fieldname": "time_out", "fieldtype": "Datetime", "width": 160},
        {"label": "Attendance", "fieldname": "attendance", "fieldtype": "Link", "options": "Attendance", "width": 140},
        {"label": "Working Hours", "fieldname": "working_hours", "fieldtype": "Float", "width": 80},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 80},
        # {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        # {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
    ]

# def get_columns():
#     return [
#         {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data","width": 120},
#         {"label": "Log Type", "fieldname": "log_type", "fieldtype": "select", "options": "IN/OUT", "width": 120},
#         {"label": "Address", "fieldname": "timeinaddress", "fieldtype": "Data","width": 120},
#         {"label": "Time", "fieldname": "time", "fieldtype": "Datetime", "width": 120},
#         {"label": "Attendance", "fieldname": "attendance", "fieldtype": "Link", "options": "Attendance", "width": 120},
#         {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
#         # {"label": "QTN Value", "fieldname": "total", "fieldtype": "Currency", "width": 100},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
#         # {"label": "Profit QPS", "fieldname": "total_offered_price", "fieldtype": "Currency", "width": 100},
#     ]


def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += f" AND eck.posting_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND eck.posting_date <= '{filters['to_date']}'"
    if filters.get("employee"):
        conditions += f" AND eck.employee = '{filters['employee']}'"
    if filters.get("company"):
        conditions += f" AND eck.company = '{filters['company']}'"

    query = f"""
        SELECT
            eck.employee,
            eck.employee_name,
            MAX(CASE WHEN eck.log_type = 'IN' THEN 'IN' END) AS log_type_in,
            MAX(CASE WHEN eck.log_type = 'IN' THEN eck.timeinaddress END) AS address_in,
            MAX(CASE WHEN eck.log_type = 'IN' THEN eck.time END) AS time_in,
            MAX(CASE WHEN eck.log_type = 'OUT' THEN 'OUT' END) AS log_type_out,
            MAX(CASE WHEN eck.log_type = 'OUT' THEN eck.timeinaddress END) AS address_out,
            MAX(CASE WHEN eck.log_type = 'OUT' THEN eck.time END) AS time_out,
            MAX(eck.attendance) AS attendance,
            MAX(att.working_hours) AS working_hours,
            MAX(att.status) AS status,
            MAX(eck.posting_date) AS posting_date,
            MAX(eck.company) AS company
        FROM
            `tabEmployee Checkin` eck
        LEFT JOIN
            `tabAttendance` att ON eck.attendance = att.name
        WHERE
            eck.docstatus = 0
            {conditions}
        GROUP BY
            eck.employee, eck.employee_name, DATE(eck.posting_date)
        ORDER BY
            eck.employee_name ASC,
            eck.time DESC
    """

    data = frappe.db.sql(query, as_dict=True)
    return data

# def get_data(filters):
#     conditions = ""
#     if filters.get("from_date"):
#         conditions += f" AND eck.posting_date >= '{filters['from_date']}'"
#     if filters.get("to_date"):
#         conditions += f" AND eck.posting_date <= '{filters['to_date']}'"
#     if filters.get("employee"):
#         conditions += f" AND eck.employee = '{filters['employee']}'"
#     if filters.get("company"):
#         conditions += f" AND eck.company = '{filters['company']}'"

#     query = f"""
#         SELECT
#             eck.employee,
#             eck.employee_name,
#             MAX(CASE WHEN eck.log_type = 'IN' THEN 'IN' END) AS log_type_in,
#             MAX(CASE WHEN eck.log_type = 'IN' THEN eck.timeinaddress END) AS address_in,
#             MAX(CASE WHEN eck.log_type = 'IN' THEN eck.time END) AS time_in,
#             MAX(CASE WHEN eck.log_type = 'OUT' THEN 'OUT' END) AS log_type_out,
#             MAX(CASE WHEN eck.log_type = 'OUT' THEN eck.timeinaddress END) AS address_out,
#             MAX(CASE WHEN eck.log_type = 'OUT' THEN eck.time END) AS time_out,
#             MAX(eck.attendance) AS attendance,
#             MAX(eck.posting_date) AS posting_date,
#             MAX(eck.company) AS company
#         FROM
#             `tabEmployee Checkin` eck
#         WHERE
#             eck.docstatus = 0
#             {conditions}
#         GROUP BY
#             eck.employee, eck.employee_name, DATE(eck.posting_date)
#         ORDER BY
#             eck.employee_name ASC,
#             eck.time DESC
#     """

#     data = frappe.db.sql(query, as_dict=True)
#     return data

# def get_data(filters):
#     conditions = ""
#     if filters.get("from_date"):
#         conditions += f" AND eck.posting_date >= '{filters['from_date']}'"
#     if filters.get("to_date"):
#         conditions += f" AND eck.posting_date <= '{filters['to_date']}'"
#     if filters.get("employee"):
#         conditions += f" AND eck.employee = '{filters['employee']}'"
#     if filters.get("company"):
#         conditions += f" AND eck.company = '{filters['company']}'"

#     query = f"""
#         SELECT
#             eck.employee,
#             eck.employee_name,
#             eck.log_type,
#             eck.timeinaddress,
#             eck.time,
#             eck.attendance,
#             eck.posting_date,
#             eck.company
#         FROM
#             `tabEmployee Checkin` eck
#         WHERE
#             eck.docstatus = 0
#             {conditions}
#             AND ((eck.log_type = 'IN' AND eck.time = (
#                     SELECT MIN(time)
#                     FROM `tabEmployee Checkin`
#                     WHERE employee = eck.employee AND log_type = 'IN' AND DATE(posting_date) = DATE(eck.posting_date)
#                 ))
#                 OR (eck.log_type = 'OUT' AND eck.time = (
#                     SELECT MAX(time)
#                     FROM `tabEmployee Checkin`
#                     WHERE employee = eck.employee AND log_type = 'OUT' AND DATE(posting_date) = DATE(eck.posting_date)
#                 )))
#         ORDER BY
#             eck.employee_name ASC,
#             eck.time DESC
#     """

#     data = frappe.db.sql(query, as_dict=True)
#     return data


# def get_data(filters):
#     conditions = ""
#     if filters.get("from_date"):
#         conditions += f" AND eck.posting_date >= '{filters['from_date']}'"
#     if filters.get("to_date"):
#         conditions += f" AND eck.posting_date <= '{filters['to_date']}'"
#     if filters.get("employee"):
#         conditions += f" AND eck.employee = '{filters['employee']}'"
#     if filters.get("company"):
#         conditions += f" AND eck.company = '{filters['company']}'"

#     # def get_data(filters):
#     # conditions = ""
#     # if filters.get("from_date"):
#     #     conditions += f" AND eck.time >= '{filters['from_date']}'"
#     # if filters.get("to_date"):
#     #     conditions += f" AND eck.time <= '{filters['to_date']}'"
#     # Add conditions for other filters like Customer, Plant based on the fields available in "Employee Checkin" doctype

#     query = f"""
#         SELECT
#             eck.employee,
#             eck.employee_name,
#             eck.log_type,
#             eck.timeinaddress,
#             eck.time,
#             eck.attendance,
#             eck.posting_date,
#             eck.company
#         FROM
#             `tabEmployee Checkin` eck
#         WHERE
#             eck.docstatus = 0
#             {conditions}
#         ORDER BY
#             eck.employee_name ASC,
#             eck.time DESC
#     """

#     data = frappe.db.sql(query, as_dict=True)
#     return data
