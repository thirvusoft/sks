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
    from frappe.custom.doctype.property_setter.property_setter import make_property_setter
    make_property_setter("Purchase Order Item", "supplier_part_no", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "image", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "pricing_rules", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "material_request_item", "Hidden", 1, "Check") 
    make_property_setter("Purchase Order Item", "sales_order_item", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "supplier_quotation_item", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "item_group", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "brand", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "item_tax_rate", "Hidden", 1, "Check") 
    make_property_setter("Purchase Order Item", "production_plan_item", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "production_plan_sub_assembly_item", "Hidden", 1, "Check")
    make_property_setter("Purchase Order", "item_price_changed", "Hidden", 1, "Check")
    make_property_setter("Purchase Order", "party_account_currency", "Hidden", 1, "Check")
    make_property_setter("Pricing Rule Detail", "margin_type", "Hidden", 1, "Check")
    make_property_setter("Pricing Rule Detail", "rate_or_discount", "Hidden", 1, "Check")
    make_property_setter("Pricing Rule Detail", "child_docname", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item Supplied", "conversion_factor", "Hidden", 1, "Check")
    make_property_setter("Purchase Order Item Supplied", "total_supplied_qty", "Hidden", 1, "Check")
    make_property_setter("Purchase Taxes and Charges", "base_total", "Hidden", 1, "Check")
    make_property_setter("Purchase Taxes and Charges", "item_wise_tax_detail", "Hidden", 1, "Check")
    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"currency_and_price_list",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"sec_warehouse",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"column_break5",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"more_info",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"subscription_section",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"terms_section_break",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"tracking_section",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"scan_barcode",
        "value":0
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"print_hide",
        'property_type':"Check",
        'field_name':"in_words",
        "value":0
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"default",
        'property_type':"Text",
        'field_name':"disable_rounded_total",
        "value":0
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"print_hide",
        'property_type':"Check",
        'field_name':"base_rounded_total",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"print_hide",
        'property_type':"Check",
        'field_name':"rounded_total",
        "value":0
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"print_hide",
        'property_type':"Check",
        'field_name':"payment_schedule",
        "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"print_hide",
        'property_type':"Check",
        'field_name':"due_date",
        "value":0
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"in_words",
        "value":0
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"rounded_total",
        "value":0
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"base_rounded_total",
        "value":0
    })
    
    purchase_order.save(ignore_permissions=True)

 