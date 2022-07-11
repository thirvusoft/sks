# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _
def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	conditions = "where si.docstatus"
	if from_date or to_date:
		if from_date and to_date:
			conditions += " and si.posting_date between '{0}' and '{1}'".format(from_date,to_date)
	report_data = frappe.db.sql(""" select count(si.name) as name,
                             		(select full_name from `tabUser` where email=si.owner) as user
										from `tabSales Invoice` as si
										{0}
										group by user
								""".format(conditions))

	columns, data = get_columns(), report_data
	return columns, data
def get_columns():
    columns = [
        _("Count") + ":Int:80",
        _("Sales User") + ":Data:100"
        ]
    return columns