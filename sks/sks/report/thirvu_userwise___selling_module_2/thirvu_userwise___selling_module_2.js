// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Thirvu Userwise - Selling Module_2"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"lable": __("From Date"),
			"fieldtype": "Date",
			"default":frappe.datetime.get_today(),
            "width": "80"
		},
		{
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
	],
};