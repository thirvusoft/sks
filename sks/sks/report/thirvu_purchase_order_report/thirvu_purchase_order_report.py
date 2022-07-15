# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    employee_name = filters.get("employee")
    conditions = "where po.docstatus"
    if from_date or to_date or employee_name:
        if from_date and to_date:
            conditions += " and po.transaction_date between '{0}' and '{1}'".format(from_date,to_date)
        if employee_name:
            conditions += " and po.owner = '{0}' ".format(employee_name)

    report_data = frappe.db.sql(""" select ROW_NUMBER() OVER (ORDER BY name),name,date,total_amount 
                             from (select po.name as name,po.transaction_date as date,
                                     po.rounded_total as total_amount
                                        from `tabPurchase Order` as po
                                        {0} )as item_details
                                """.format(conditions))

    columns, data = get_columns(), report_data
    return columns, data
def get_columns():
    columns = [
        _("PO No") + ":int:80",
        _("Invoices No") + ":Data:130",
        _("Date") + ":Date:130",
        _("Total Amount") + ":Currency:130",
             
        ]
    return columns