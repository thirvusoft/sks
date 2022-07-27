import frappe
from frappe import _
@frappe.whitelist()
def stock_details_validation(doc,event):
    if doc.ts_is_closing_stock_detail:
        if not doc.ts_closing_stock_details_table:
            frappe.throw(_("Closing Stock Details Is Empty"))


@frappe.whitelist()
def item_warehouse_fetching(item_name,ts_company):
    check = 1
    item_name =  frappe.get_doc("Item",item_name)
    for warehouse in item_name.warehouse:
        if warehouse.company == ts_company:
            check = 0
            return warehouse.storebin
        else:
            check = 1
    if check==1:
        return 0