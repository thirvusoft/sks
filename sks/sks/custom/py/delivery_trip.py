import frappe
import json
@frappe.whitelist()
def get_sales_invoice(territory,date):
    salesorder = frappe.get_all("Sales Order",filters = {"delivery_date":date},pluck = 'name')
    frappe.errprint(salesorder)
    sales_invoice = frappe.get_all("Sales Invoice Item",filters = {"sales_order":["in",salesorder]},pluck = 'parent')
    frappe.errprint(sales_invoice)
    sales = frappe.get_all("Sales Invoice",fields=['name','customer_address','customer','delivery_status','reason'],filters ={'territory':territory,'name':['in',sales_invoice]})
    # sales =  frappe.db.sql('''
    # select name as sales_invoice, customer_address as address, customer, delivery_status from `tabSales Invoice` where territory = "{0}" and name in ({1})
    # '''.format(territory,*sales_invoice),as_dict = 1)
    frappe.errprint(sales)
    return sales
@frappe.whitelist()
def update_invoice(invoice,fields):
    fields = json.loads(fields)
    frappe.errprint(fields['reason'])
    frappe.db.set_value("Sales Invoice",invoice, 'delivery_status', fields['delivery_status'])
    frappe.db.set_value("Sales Invoice",invoice, 'reason', fields['reason'])
    frappe.db.commit()
    return ""
    
