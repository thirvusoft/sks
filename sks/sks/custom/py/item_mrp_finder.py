import frappe
@frappe.whitelist()
def ts_mrp_finder(ts_item_code):
	try:
		ts_item = frappe.get_last_doc("Item Price", {"item_code": ts_item_code,"selling":1})
		item_mrp=ts_item.ts_mrp
		item_selling_price=ts_item.price_list_rate
		return item_mrp,item_selling_price
	except:
		pass
