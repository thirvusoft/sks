import frappe
from sks.sks.utils.buying.purchase_order.purchase_order_item.purchase_order_item_custom import purchase_order_item_property_setter,purchase_order_item_custom_fields
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_order_customization():
          purchase_order_item_property_setter()
          purchase_order_item_custom_fields()
          purchase_order_custom_field()
          purchase_order_property_setter()
def purchase_order_custom_field():      
          custom_fields = {
                    "Purchase Order": [
                    dict(
                    label= "Place of Supply",
                    fieldname= "place_of_supply",
                    insert_after= "company_shipping_address",
                    fieldtype="Data",
                    read_only= 1,
                    print_hide= 1,
                    ),
                    dict(
                    label= "Item Price Changed",
                    fieldname= "item_price_changed",
                    insert_after= "base_net_total",
                    fieldtype= "Text",
                    read_only= 1,
                    hidden=1,
                    )                
                    ],
          }
          create_custom_fields(custom_fields)
def purchase_order_property_setter():                
    make_property_setter("Purchase Order", "item_price_changed", "hidden", 1,"Check")
    make_property_setter("Purchase Order", "party_account_currency", "hidden", 1,"Check")
    make_property_setter("Purchase Order", "apply_tds", "hidden", 1, "Check")
    make_property_setter("Purchase Order", "order_confirmation_no", "hidden", 1,"Check")
    make_property_setter("Purchase Order", "accounting_dimensions_section", "hidden", 1,"Check")
    make_property_setter("Purchase Order", "advance_paid", "hidden", 1,"Check")
    make_property_setter("Purchase Order", "disable_rounded_total", "hidden", 1,"Check")
    make_property_setter("Purchase Order", "disable_rounded_total", "default", 1,"Text")
    make_property_setter("Purchase Order", "rounding_adjustment", "hidden", 1,"Check")
    make_property_setter("Purchase Order", "total_net_weight", "hidden", 1,"Check")
    
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
    "value":1
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
    'property_type':"Check",
    'field_name':"disable_rounded_total",
    "value":1
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

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"reqd",
    'field_name':"schedule_date",
    "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"default",
    'field_name':"naming_series",
    "value":"PUR-ORD-.YYYY.-"
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"hidden",
    'field_name':"naming_series",
    "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"hidden",
    'property_type':"Check",
    'field_name':"before_items_section",
    "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"hidden",
    'property_type':"Section Break",
    'field_name':"taxes_section",
    "value":1
    })
    
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"hidden",
    'property_type':"Check",
    'field_name':"section_break_52",
    "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"hidden",
    'property_type':"Check",
    'field_name':"total",
    "value":1
    })
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"hidden",
    'property_type':"Check",
    'field_name':"discount_section",
    "value":1
    })
    
    purchase_order.save(ignore_permissions=True)

    purchase_order=frappe.get_doc({
    'doctype':'Property Setter',
    'doctype_or_field': "DocField",
    'doc_type': "Purchase Order",
    'property':"hidden",
    'property_type':"Check",
    'field_name':"payment_schedule_section",
    "value":1
    })
    
    purchase_order.save(ignore_permissions=True)