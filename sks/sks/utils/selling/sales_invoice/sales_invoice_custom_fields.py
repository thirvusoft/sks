import frappe
from sks.sks.utils.selling.sales_invoice.sales_invoice_item.sales_invoice_item_custom_fields import sales_invoice_item_property_setter,sales_invoice_item_custom_fields
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def sales_invoice_customization():
    sales_invoice_item_property_setter()
    sales_invoice_item_custom_fields()
    sales_invoice_custom_field()
    sales_invoice_property_setter()

def sales_invoice_custom_field():
    custom_fields={
        "Sales Invoice":[
            dict(fieldname='time_of_delivery',
                label='Time of Delivery',
                fieldtype='Time',
                insert_after='delivery_status',
                hidden=1,
                allow_on_submit=1
            ),
            dict(fieldname='delivery_status',
                label='Delivery Status',
                fieldtype='Select',
                insert_after='due_date',
                allow_on_submit=1,
                options="\nAttempt\nDelivered\nNot Delivered\nReady To Dispatch\nHold\nOut to Delivery\nReattempt\nReturned"
            ),
            dict(fieldname='reason',
                label='Reason',
                fieldtype='Data',
                insert_after='time_of_delivery',
                allow_on_submit=1
            ),
            dict(fieldname='scan_barcode_to_verify_the_items',
                label='Scan Barcode To Verify The Items',
                fieldtype='Data',
                insert_after='scan_barcode',
                options="Barcode",
                hidden=1
            ),
            dict(fieldname='mode_of_delivery',
                label='Mode of Delivery',
                fieldtype='Select',
                options='\nPick Up\nDoor Delivery',
                insert_after='reason',
                fetch_from="Sales Order.mode_of_delivery",
                read_only=1
            ),
            dict(fieldname='due_day',
                label='Payment Due Day',
                fieldtype='Data',
                insert_after='due_date',
                read_only=1
            ),
            dict(fieldname='your_savings',
                label='Your Savings',
                fieldtype='Currency',
                insert_after='grand_total',
                read_only=1
            ),
            dict(fieldname='billed_by',
                label='Billed By',
                fieldtype='Data',
                insert_after='pos_profile',
                read_only=1
            ),
            dict(fieldname='bill_barcode',
                label='Bill Barcode',
                fieldtype='Barcode',
                insert_after='reason',
                read_only=1,
                hidden=1
            ),
            dict(fieldname='is_local_delivery',
                label='Is Local Delivery',
                fieldtype='Check', 
                insert_after='mode_of_delivery',
                read_only=1,
                depends_on="eval:doc.mode_of_delivery=='Door Delivery'"
            ),
            dict(fieldname='payment_type',
                label='Payment Type',
                fieldtype='Select',
                options=' \nDue Bill\nCredit Bill',
                insert_after='is_local_delivery',
                reqd=0,no_copy=0
            ),
            dict(fieldname='mode_of_payment',
                label='Mode of Payment',
                fieldtype='Data', 
                insert_after='billed_by',
                hidden=1,
            )
        ],
    }
    create_custom_fields(custom_fields)

def sales_invoice_property_setter():
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Check",
        'field_name':"is_debit_note",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"customer_po_details",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"time_sheet_list",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"subscription_section",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"section_break2",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"sales_team_section_break",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"more_information",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"gst_section",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"edit_printing_settings",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"transporter_info",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"terms_section_break",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"payment_schedule_section",
        "value":"1"
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"advances_section",
        "value":'1'
    })
    ts_new.save(ignore_permissions=True)
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"loyalty_points_redemption",
        "value":'1'
    })
    ts_new.save(ignore_permissions=True)
    
    make_property_setter("Sales Invoice", "column_break4", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "posa_additional_notes_section", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "more_info", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "rounding_adjustment", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "total_advance", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "project", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "shipping_rule", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "scan_barcode", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "update_stock", "hidden", 1, "Check")
    make_property_setter("Sales Invoice", "currency_and_price_list", "hidden", 1, "Section Break")
    make_property_setter("Sales Invoice", "section_break_49", "hidden", 1, "Section Break")
    make_property_setter("Sales Invoice", "cost_center", "default", "Main - SKS", "Link")




