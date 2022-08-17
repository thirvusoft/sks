import frappe
from sks.sks.utils.selling.delivery_note.packed_item.packed_item_custom_fields import packed_item_customization
from sks.sks.utils.selling.delivery_note.delivery_note_item.delivery_note_item_custom_fields import delivery_note_item_property_setter,delivery_note_item_custom_fields
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def delivery_note_customization():
    delivery_note_item_property_setter()
    delivery_note_item_custom_fields()
    delivery_note_custom_field()
    delivery_note_property_setter()
    packed_item_customization()
def delivery_note_custom_field():
    custom_fields={
        "Delivery Note":[
            dict(fieldname='scan_barcode_to_verify_the_items',
                label='Scan Barcode To Verify The Items',
                fieldtype='Data', 
                insert_after='scan_barcode',
                options="Barcode",
                hidden=0
            ),
            dict(fieldname='mode_of_delivery', 
                label='Mode of Delivery',
                fieldtype='Select', 
                insert_after='customer',
                options='\nPick Up\nDoor Delivery',
                read_only=1,
                fetch_from="Sales Order.mode_of_delivery"
            ),
            dict(fieldname='delivery_day',
                label='Delivery day',
                fieldtype='Data',
                insert_after='mode_of_delivery',
                read_only=1
            ),
            dict(fieldname='outstanding_amount', 
                label='Outstanding Amount',
                fieldtype='Currency', 
                insert_after='total_qty',
                read_only=1
            ),
            dict(fieldname='outstanding_amount_and_total_amount', 
                label='Outstanding Amount and Total Amount',
                fieldtype='Currency', 
                insert_after='outstanding_amount',
                read_only=1
            ),
            dict(fieldname='posting_day', label='Posting Day',
                fieldtype='Data', 
                insert_after='posting_date', 
                read_only=1
            ),
            dict(fieldname='is_local_delivery',
                label='Is Local Delivery',
                fieldtype='Check', 
                insert_after='mode_of_delivery',
                read_only=1,
                depends_on="eval:doc.mode_of_delivery=='Door Delivery'"
            ),
            dict(fieldname='is_against_sales_invoice',
                label='Is Against Sales Invoice',
                fieldtype='Check', 
                insert_after='is_local_delivery',
                read_only=1,
                hidden=1,
                no_copy=1,
                allow_on_submit=1
            ),
            dict(fieldname='is_first_onload',
                label='Is First Onload',
                fieldtype='Check', 
                insert_after='is_against_sales_invoice',
                read_only=1,
                hidden=1,
                no_copy=1
            )
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
    make_property_setter("Delivery Note", "customer_po_details", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "currency_and_price_list", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "sec_warehouse", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "scan_barcode", "hidden", "1", "Data")
    make_property_setter("Delivery Note", "taxes_section", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "sec_tax_breakup", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "section_break_49", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "section_break_41", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "accounting_dimensions_section", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "section_break_44", "hidden", "1", "Section Break")
    make_property_setter("Delivery Note", "totals", "hidden", "1", "Section Break")