import frappe
@frappe.whitelist()
def ts_mrp_finder(ts_item_code):
	ts_item=frappe.get_doc("Item",ts_item_code)
	return ts_item.mrp