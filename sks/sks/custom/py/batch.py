import frappe
def item_price_creator(doc,action):
	if doc.reference_doctype=="Purchase Receipt":
		ts_new_item_price=frappe.get_doc({
			"doctype":"Item Price",
			"item_code":doc.item,
			"price_list":"Standard Selling",
			"batch_no":doc.name,
			"price_list_rate":doc.ts_selling_price
		})
		ts_new_item_price.insert()
		ts_new_item_price.save()
