import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter




def sales_order_item_customization():
    sales_order_item_custom_fields()
    sales_order_item_property_setter()
   

def sales_order_item_custom_fields():
    custom_fields={
        "Sales Order Item":[
             dict(fieldname='ts_warehouse', label='TS Warehouse',
                fieldtype='Data',hidden=0, insert_after='gros_profit'),
           ]
        }
    create_custom_fields(custom_fields)

def sales_order_item_property_setter():
    make_property_setter("Sales Order Item", "section_break_63", "hidden", "1", "Section Break")
    make_property_setter("Sales Order Item", "work_order_qty", "hidden", "1", "Float")
    make_property_setter("Sales Order Item", "produced_qty", "hidden", "1", "Float")
    make_property_setter("Sales Order Item", "against_blanket_order", "hidden", "1", "Check")
    make_property_setter("Sales Order Item", "drop_ship_section", "hidden", "1", "Section Break")
    make_property_setter("Sales Order Item", "is_nil_exempt", "hidden", "1", "Check")
    make_property_setter("Sales Order Item", "is_non_gst", "hidden", "1", "Check")
    make_property_setter("Sales Order Item", "ensure_delivery_based_on_produced_serial_no", "hidden", "1", "Check")
    make_property_setter("Sales Order Item", "shopping_cart_section", "hidden", "1", "Section Break")