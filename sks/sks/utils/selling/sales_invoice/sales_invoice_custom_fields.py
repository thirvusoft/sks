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
            dict(fieldname='time_of_delivery', label='Time of Delivery',
                fieldtype='Time', insert_after='delivery_status',hidden=1,allow_on_submit=1),
            dict(fieldname='delivery_status', label='Delivery Status',
                fieldtype='Select', insert_after='due_date',default="Ready To Dispatch",
                options="Attempt\nDelivered\nNot Delivered\nReady To Dispatch\nReattempt\nReturned"),
            dict(fieldname='reason', label='Reason',
                fieldtype='Data', insert_after='time_of_delivery', allow_on_submit=1),
            dict(fieldname='scan_barcode_to_verify_the_items', label='Scan Barcode To Verify The Items',
                fieldtype='Data', insert_after='scan_barcode',options="Barcode",hidden=1,),
            dict(fieldname='mode_of_delivery', label='Mode of Delivery',
                fieldtype='Data', insert_after='reason',fetch_from="Sales Order.mode_of_delivery",read_only=1,),
            dict(fieldname='due_day', label='Payment Due Day',
                fieldtype='Data', insert_after='due_date',read_only=1)
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
    make_property_setter("Sales Invoice", "column_break4", "hidden", "1", "Section Break")

