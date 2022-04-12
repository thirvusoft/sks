import frappe
@frappe.whitelist()
def ts_supplier_items_finder(ts_supplier):
    ts_supplier_matched_item=[]
    ts_total_item_details=frappe.db.get_all("Item")
    for ts_item_name in ts_total_item_details:
        ts_item_detail=frappe.get_doc("Item",ts_item_name)
        if(ts_item_detail.__dict__["supplier_items"]):
            ts_supplire_length=len(ts_item_detail.__dict__["supplier_items"])
            for ts_i in range(0,ts_supplire_length,1):
                if(ts_item_detail.__dict__["supplier_items"][ts_i].__dict__["supplier"]==ts_supplier):
                    ts_supplier_matched_item.append(ts_item_name["name"])
    if(ts_supplier_matched_item):
        return ts_supplier_matched_item
    else:
        frappe.msgprint("There Is No Item For Supplier : "+ts_supplier)