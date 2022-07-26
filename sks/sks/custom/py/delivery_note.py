import frappe
@frappe.whitelist()
def item_check_with_sales_order(item_code_checking=None,checking_sales_order=None):
	matched_item=0
	item_code_from_sales_order=frappe.get_doc("Sales Order",checking_sales_order)
	total_item=item_code_from_sales_order.__dict__["items"]
	len_items=len(total_item)
	if(item_code_checking != None):
		for j in range(0,len_items,1):
			if(item_code_checking == total_item[j].__dict__["item_code"]):
				item_code=total_item[j].__dict__["item_code"]
				matched_item=matched_item+1
				break
	if(matched_item==1):
		matched_item=0
		return item_code
	else:
		return 0


@frappe.whitelist()
def item_warehouse_fetching(item_code,company):
    itemname =  frappe.get_doc("Item",item_code)

    warehouse = frappe.db.get_value("Item Warehouse" ,{'company':company},'storebin')
    return warehouse

def warehouse_fetcing(doc,event):
    item = doc.items
    for i in item:
        i.warehouse = i.ts_warehouse