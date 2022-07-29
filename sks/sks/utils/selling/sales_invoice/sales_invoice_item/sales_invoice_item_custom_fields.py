import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def sales_invoice_item_custom_fields():
    custom_fields={
        "Sales Invoice Item":[
                dict(fieldname='item_verified', label='Item Verified',
                fieldtype='Check', insert_after='mrp',read_only=1,in_list_view=1,columns=2),
                dict(fieldname='ts_warehouse', label='TS Warehouse',
                fieldtype='Data', insert_after='warehouse',read_only=1),
                dict(fieldname='mrp', label='MRP',
                fieldtype='Currency', insert_after='amount',read_only=1,fetch_from="item_code.mrp"),
        ],
    }
    create_custom_fields(custom_fields)

def sales_invoice_item_property_setter():
    make_property_setter("Sales Invoice Item", "is_nil_exempt", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "allow_zero_valuation_rate", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "is_non_gst", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "drop_ship", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "accounting", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "deferred_revenue", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "edit_references", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "section_break_54", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "description_section", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "posa_notes", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "section_break_18", "hidden", 1, "Check")
    make_property_setter("Sales Invoice Item", "project", "hidden", 1, "Check")
