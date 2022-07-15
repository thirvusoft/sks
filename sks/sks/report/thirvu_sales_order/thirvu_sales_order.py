# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _
def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	employee_name = filters.get("employee")
	conditions = "where so.docstatus"
	if from_date or to_date or employee_name:
		if from_date and to_date:
			conditions += " and so.transaction_date between '{0}' and '{1}'".format(from_date,to_date)
		if employee_name:
			conditions += " and so.owner = '{0}' ".format(employee_name)

	report_data = frappe.db.sql(""" select ROW_NUMBER() OVER (ORDER BY name),name,date,total_amount 
                             from (select so.name as name,so.transaction_date as date,
                                     so.rounded_total as total_amount
                                        from `tabSales Order` as so
                                        {0} )as item_details
                                """.format(conditions))

	columns, data = get_columns(), report_data
	return columns, data
def get_columns():
    columns = [
        _("SO No") + ":Int:80",
        _("Invoices No") + ":Data:130",
        _("Date") + ":Date:130",
        _("Total Amount") + ":Currency:130",
     
          
        ]
    return columns