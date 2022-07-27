import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def delivery_note_item_custom_fields():
    custom_fields={
        "Delivery Note Item":[
            dict(fieldname='item_verified', label='Item Verified',
                fieldtype='Check', insert_after='amount',options="Barcode",in_list_view=1,columns=2,read_only=1),
              dict(fieldname='ts_warehouse', label='TS Warehouse',
                fieldtype='Data',hidden=1, insert_after='warehouse')

        ]
    }
    create_custom_fields(custom_fields)

def delivery_note_item_property_setter():
    make_property_setter("Delivery Note Item", "is_nil_exempt", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "is_non_gst", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "section_break_72", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note Item", "allow_zero_valuation_rate", "hidden", "1", "Check")
