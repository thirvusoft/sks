import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def execute():
    custom_fields = {
        "Purchase Order": [
            dict(
                fieldname='supplier_gstin',
                label='Supplier GSTIN',
                read_only= 1,
                print_hide= 1,
                fieldtype='Data',
                insert_after='supplier_address',
                hidden=1,
                allow_on_submit=0,
                fetch_form='supplier_address.gstin',
            ),
            dict(     
                fetch_from= "shipping_address.gstin",
                label= "Company GSTIN",
                fieldname= "company_gstin",
                insert_after= "shipping_address_display",
                fieldtype="Data",
                allow_on_submit=0,
                read_only= 1,
                translatable= 1,
                print_hide= 1,
            ),
            dict(
                label= "Place of Supply",
                fieldname= "place_of_supply",
                insert_after= "company_shipping_address",
                fieldtype="Data",
                allow_on_submit=0,
                read_only= 1,
                translatable= 1,
                print_hide= 1,
            ),
            dict(
                label= "Item Price Changed",
                fieldname= "item_price_changed",
                insert_after= "base_net_total",
                fieldtype= "Text",
                allow_on_submit=0,
                read_only= 1,
                hidden=1,
                translatable= 1,
            )
            
        ],
        "Purchase Order Item": [
            dict(
                allow_on_submit= 1,
                fetch_from= "item_code.gst_hsn_code",
                fetch_if_empty= 1,
                fieldname= "gst_hsn_code",
                fieldtype= "Data",
                insert_after= "description",
                label= "HSN/SAC",
                print_hide= 1,
                translatable= 1,
                unique= 0,
            ),
            dict(
                fetch_from= "item_code.is_nil_exempt",
                fieldname= "is_nil_exempt",
                fieldtype= "Check",
                insert_after= "gst_hsn_code",
                label= "Is Nil Rated or Exempted",
                print_hide= 1,
                translatable= 1,
            ),
            dict(
                fetch_from= "item_code.is_non_gst",
                fieldname= "is_non_gst",
                fieldtype= "Check",
                insert_after= "is_nil_exempt",
                label= "Is Non GST",
                print_hide= 1,
                translatable= 1,
            ),
            dict(
                fieldname= "ts_mrp",
                fieldtype= "Currency",
                in_list_view= 1,
                insert_after= "sec_break2",
                label= "MRP",
            ),
            
        ],
    }
    create_custom_fields(custom_fields)
    
# def sales_invoice(doc,event):
#     ts_field=frappe.get_doc({
#           "doctype":"Custom Field",
#           "dt":"Purchase Order",
#           "label":"Supplier GSTIN",
#           "fieldname":"supplier_gstin",
#           "insert_after":"supplier_address",
#           "fetch_from": "supplier_address.gstin",
#           "fieldtype":"Time",
#           "read_only": 1,
#           "allow_on_submit":0,
#           "print_hide": 1,
#           "translatable": 1,

#     })
#     ts_field.save()
#     ts_field=frappe.get_doc({
       
#     })
#     ts_field.save()
#     ts_field=frappe.get_doc({
#           "doctype":"Custom Field",
#           "dt": "Purchase Order",
#           "fetch_from": "shipping_address.gstin",
#           "label": "Company GSTIN",
#           "fieldname": "company_gstin",
#           "insert_after": "shipping_address_display",
#           "fieldtype":"Data",
#           "allow_on_submit":0,
#           "read_only": 1,
#           "translatable": 1,
#           "print_hide": 1,
#     })
#     ts_field.save()
#     ts_field=frappe.get_doc({
#           "doctype":"Custom Field",
#           "dt": "Purchase Order",
#           "label": "Place of Supply",
#           "fieldname": "place_of_supply",
#           "insert_after": "company_shipping_address",
#           "fieldtype":"Data",
#           "allow_on_submit":0,
#           "read_only": 1,
#           "translatable": 1,
#           "print_hide": 1,
#     })
#     ts_field.save()
#     ts_field=frappe.get_doc({
#           "doctype":"Custom Field",
#           "dt": "Purchase Order",
#           "label": "Item Price Changed",
#           "fieldname": "item_price_changed",
#           "insert_after": "base_net_total",
#           "fieldtype": "Text",
#           "allow_on_submit":0,
#           "read_only": 1,
#           "hidden":1,
#           "translatable": 1,
#     })
#     ts_field.save()

#--------------------------Property Setter--------------------------
    from frappe.custom.doctype.property_setter.property_setter import make_property_setter
    make_property_setter("Purchase Order Item", "amount", "property", 1, "Int")
    make_property_setter("Purchase Order Item", "amount", "property", 1, "Int")
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

 