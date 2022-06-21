import frappe
def property_setter():
    sales_invoice()

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