import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def property_setter():
    sales_invoice()
    purchase_invoice()

def sales_invoice():
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Check",
        'field_name':"is_debit_note",
        "value":"1"
    })
    ts_new.save(),
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"customer_po_details",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"time_sheet_list",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"subscription_section",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"section_break2",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"sales_team_section_break",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"more_info",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"gst_section",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"edit_printing_settings",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"transporter_info",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"terms_section_break",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"payment_schedule_section",
        "value":"1"
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"advances_section",
        "value":'1'
    })
    ts_new.save()
    ts_new=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Sales Invoice",
        'property':"hidden",
        "property_type":"Section Break",
        'field_name':"loyalty_points_redemption",
        "value":'1'
    })
    ts_new.save()

def purchase_invoice():
    make_property_setter("Sales Invoice", "party_account_currency", "hidden", "1", "Link")
    make_property_setter("Sales Invoice", "subscription_section", "hidden", "1", "Section Break")
    make_property_setter("Sales Invoice", "accounting_dimensions_section", "hidden", "1", "Section Break")
    make_property_setter("Sales Invoice", "supplier_invoice_details", "hidden", "1", "Section Break")
    make_property_setter("Sales Invoice", "update_stock", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "scan_barcode", "hidden", "1", "Data")
    make_property_setter("Sales Invoice", "terms_section_break", "hidden", "1", "Section Break")
    make_property_setter("Sales Invoice", "more_info", "hidden", "1", "Section Break")
    make_property_setter("Sales Invoice", "accounting_details_section", "hidden", "1", "Section Break")