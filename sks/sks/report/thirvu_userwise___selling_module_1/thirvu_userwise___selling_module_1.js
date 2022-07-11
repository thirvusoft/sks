// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Thirvu Userwise - Selling Module_1"] = {
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
		{
			"fieldname":"employee",
            "label": __("Employee Name"),
            "fieldtype": "Data",
			"read_only":1,
		}
	],
	onload: function(report){
		frappe.query_report.set_filter_value("employee",frappe.session.user);
	}
};