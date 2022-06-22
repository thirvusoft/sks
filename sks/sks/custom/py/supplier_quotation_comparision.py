import frappe
from frappe.utils import flt
from frappe import _, errprint
from frappe.model.mapper import get_mapped_doc
@frappe.whitelist()
def make_purchase_order(source_name,r_date,target_doc=None):
    def set_missing_values(source,target):
        target.run_method("set_missing_values") 
        target.run_method("calculate_taxes_and_totals")
        target.schedule_date = r_date
        errprint(target.schedule_date)
    def update_item(obj, target, source_parent):
        target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)
    doclist = get_mapped_doc("Supplier Quotation",source_name,{
			"Supplier Quotation": {
				"doctype": "Purchase Order",
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Supplier Quotation Item": {
				"doctype": "Purchase Order Item",
				"field_map": [
					["name", "supplier_quotation_item"],
					["parent", "supplier_quotation"],
					["material_request", "material_request"],
					["material_request_item", "material_request_item"],
					["sales_order", "sales_order"],
				],
				"postprocess": update_item,
			},
			"Purchase Taxes and Charges": {
				"doctype": "Purchase Taxes and Charges",
			},
		},
		target_doc,
		set_missing_values,
	)
    doclist.set_onload("ignore_price_list", True)
    doclist.save()
    frappe.msgprint("Purchase Order has been raised against the supplier")
    doclist.submit()
    frappe.db.commit()
