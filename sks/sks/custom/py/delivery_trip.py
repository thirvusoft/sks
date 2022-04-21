import frappe
@frappe.whitelist()
def get_sales_invoice(territory):
    sales =  frappe.db.sql('''
    select name as sales_invoice, customer_address as address, customer, delivery_status from `tabSales Invoice` where territory = "{0}"
    '''.format(territory),as_dict = 1)
    frappe.errprint(sales)
    return sales