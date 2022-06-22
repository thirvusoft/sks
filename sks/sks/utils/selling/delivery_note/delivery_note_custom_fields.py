import frappe
from sks.sks.utils.selling.delivery_note.delivery_note_item.delivery_note_item_custom_fields import delivery_note_item_property_setter,delivery_note_item_custom_fields
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def delivery_note_customization():
    delivery_note_item_property_setter()
    delivery_note_item_custom_fields()
    delivery_note_custom_field()
    delivery_note_property_setter()

def delivery_note_custom_field():
    custom_fields={
        "Delivery Note":[
            dict(fieldname='scan_barcode_to_verify_the_items',
                label='Scan Barcode To Verify The Items',
                fieldtype='Data', 
                insert_after='column_break_54',
                options="Barcode",
                hidden=1),
            dict(fieldname='mode_of_delivery', 
                label='Mode of Delivery',
                fieldtype='Data', 
                insert_after='customer',
                options="Barcode",
                read_only=1,
                fetch_from="Sales Order.mode_of_delivery"),
            dict(fieldname='outstanding_amount', 
                label='Outstanding Amount',
                fieldtype='Currency', 
                insert_after='total_qty',
                read_only=1),
            dict(fieldname='outstanding_amount_and_total_amount', 
                label='Outstanding Amount and Total Amount',
                fieldtype='Currency', 
                insert_after='outstanding_amount',
                read_only=1),
        ]
    }
    create_custom_fields(custom_fields)

def delivery_note_property_setter():
    make_property_setter("Delivery Note", "pick_list", "hidden", "1", "Link")
    make_property_setter("Delivery Note", "contact_mobile", "hidden", "1", "Small Text")
    make_property_setter("Delivery Note", "contact_email", "hidden", "1", "Data")
    make_property_setter("Delivery Note", "section_break1", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "sales_team_section_break", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "subscription_section", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "section_break_83", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "printing_details", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "more_info", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "transporter_info", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "terms_section_break", "hidden", "1", "Section Break")