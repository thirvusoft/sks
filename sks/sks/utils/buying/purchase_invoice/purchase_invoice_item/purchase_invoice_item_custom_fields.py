import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_invoice_item_custom_fields():
	custom_fields = {
		"Purchase Invoice Item":[
			dict(
				fieldname='barcode', 
				label='Barcode',
				fieldtype='Data', 
				insert_after='item_code',
			),
			dict(
				fieldname='expiry_date', 
				label='Expiry Date',
				fieldtype='Date', 
				insert_after='rejected_qty',
				in_list_view=1,
				columns=1,
				reqd=0
			),
			dict(
				fieldname='item_verified', 
				label='Item Verified',
				fieldtype='Check', 
				insert_after='amount',
				in_list_view=1,
				columns=1,
				read_only=1
			),
			dict(
				fieldname='ts_mrp', 
				label='MRP',
				fieldtype='Currency', 
				insert_after='expiry_date',
				in_list_view=1,
				columns=1,
				reqd=0
			),
			dict(
				fieldname='ts_selling_rate', 
				label='Selling Rate',
				fieldtype='Currency', 
				insert_after='ts_mrp',
				in_list_view=1,
				columns=1,
				read_only=0
			),
			dict(
				fieldname='ts_selling_rate_automatic_calculation', 
				label='Selling Rate Automatic Calculation',
				fieldtype='Check', 
				insert_after='ts_selling_rate',
				read_only=1,
				hidden=1,
				no_copy=1
			),
			dict(
				fieldname='ts_valuation_rate', 
				label='Valuation Rate',
				fieldtype='Currency', 
				insert_after='conversion_factor', 
				read_only=1
			),

			dict(
				fieldname='ts_warehouse',
				label='TS Warehouse',
				fieldtype='Data', 
				hidden=1,
				insert_after='warehouse'
			),
			dict(
				fieldname='is_free_item_from_supplier', 
				label='Free Item From Supplier',
				fieldtype='Check', 
				insert_after='item_code',		
			),
		],
	}
	create_custom_fields(custom_fields)

def purchase_invoice_item_property_setter():
    make_property_setter("Purchase Invoice Item", "is_nil_exempt", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "is_non_gst", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "section_break_82", "hidden", 1, "Section Break")
    make_property_setter("Purchase Invoice Item", "manufacture_details", "hidden", 1, "Section Break")
    make_property_setter("Purchase Invoice Item", "accounting", "hidden", 1, "Section Break")
    make_property_setter("Purchase Invoice Item", "deferred_expense_section", "hidden", 1, "Section Break")
    make_property_setter("Purchase Invoice Item", "reference", "hidden", 1, "Section Break")
    make_property_setter("Purchase Invoice Item", "serial_no", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "allow_zero_valuation_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "item_weight_details", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "bom", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "rejected_serial_no", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "base_net_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "base_net_amount", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "landed_cost_voucher_amount", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "stock_uom_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice Item", "project", "hidden", 1, "Check")
