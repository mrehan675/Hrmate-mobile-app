// Copyright (c) 2024, rehan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Attendance Report"] = {
	"filters": [
		{
		  "fieldname": "company",
		  "label": __("Company"),
		  "fieldtype": "Link",
		  "options": "Company",
		  "default": frappe.defaults.get_user_default("Company"),
		//   "reqd": 1
		},
		{
		  "fieldname": "from_date",
		  "label": __("From Date"),
		  "fieldtype": "Date",
		  "default": frappe.datetime.get_today(),
		  "reqd": 1,
		  "width": "60px"
		},
		{
			"fieldname": "to_date",
			"label": __("TO Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			// "default": frappe.defaults.get_user_default("Company"),
			// "reqd": 1
		}
		  
	],
	"formatter": function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === 'working_hours') {
            var working_hours = parseFloat(data.working_hours);
            if (working_hours < 9) {
                value = "<span style='color:red'>" + value + "</span>";
            } else if (working_hours > 10) {
                value = "<span style='color:green'>" + value + "</span>";
            }
        }
        return value;
    }
};
// 	"formatter": function (value, row, column, data, default_formatter) {
//         value = default_formatter(value, row, column, data);
//         if (column.fieldname === 'working_hours' && parseFloat(data.working_hours) < 9) {
//             value = "<span style='color:red'>" + value + "</span>";
//         }
//         return value;
//     }
// };
// };
