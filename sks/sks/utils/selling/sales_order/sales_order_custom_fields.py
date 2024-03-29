import frappe
from sks.sks.utils.selling.sales_order.sales_order_item.sales_order_item_custom_fields import sales_order_item_property_setter,sales_order_item_custom_fields
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def sales_order_customization():
    sales_order_item_property_setter()
    sales_order_item_custom_fields()
    sales_order_custom_field()
    sales_order_property_setter()

def sales_order_custom_field():
    custom_fields={
        "Sales Order":[
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
                hidden=1
            ),
            dict(fieldname='mode_of_delivery',
                label='Mode of Delivery',
                fieldtype='Select',
                options=' \nPick Up\nDoor Delivery',
                insert_after='order_type',
                reqd=1
            ),
            dict(fieldname='delivery_day',
                label='Delivery day',
                fieldtype='Data',
                insert_after='delivery_date',
                read_only=1
            ),
            dict(fieldname='is_against_delivery_note',
                label='Is Against Delivery Note',
                fieldtype='Check',
                allow_on_submit=1,
                insert_after='posting_day', 
                hidden=1,
                no_copy=1
            ),
            dict(fieldname='is_local_delivery', 
                label='Is Local Delivery',
                fieldtype='Check',
                insert_after='payment_type',
                depends_on="eval:doc.mode_of_delivery=='Door Delivery'"
            ),
            dict(fieldname='payment_type',
                label='Payment Type',
                fieldtype='Select',
                options='\nDue Bill\nCredit Bill',
                insert_after='mode_of_delivery',
                reqd=0,no_copy=0
            ),
            dict(fieldname='print_with_price', 
                label='Print With Price',
                fieldtype='Check',
                insert_after='is_local_delivery',
                default="1",
                no_copy=1
            ),
            dict(fieldname='customer_details', 
                label='Customer Details',
                fieldtype='Code',
                insert_after='delivery_day',
                no_copy=1,
                read_only=1
            )

        ]
    }
    create_custom_fields(custom_fields)

def sales_order_property_setter():
    make_property_setter("Sales Order", "po_no", "hidden", "1", "Check")
    make_property_setter("Sales Order", "order_type", "hidden", "1", "Check")
    make_property_setter("Sales Order", "ignore_pricing_rule", "hidden", "1", "Check")
    make_property_setter("Sales Order", "more_info", "hidden", "1", "Check")
    make_property_setter("Sales Order", "printing_details", "hidden", "1", "Check")
    make_property_setter("Sales Order", "section_break_78", "hidden", "1", "Check")
    make_property_setter("Sales Order", "sales_team_section_break", "hidden", "1", "Check")
    make_property_setter("Sales Order", "section_break1", "hidden", "1", "Check")
    make_property_setter("Sales Order", "subscription_section", "hidden", "1", "Check")
    make_property_setter("Sales Order", "taxes_section", "hidden", "1", "Check")
    make_property_setter("Sales Order", "taxes_and_charges", "hidden", "1", "Check")
    make_property_setter("Sales Order", "taxes", "hidden", "1", "Check")
    make_property_setter("Sales Order", "sec_tax_breakup", "1","hidden", "Check")
    make_property_setter("Sales Order", "ts_tax_breakup", "1", "hidden", "Check")
    make_property_setter("Sales Order", "scan_barcode", "hidden", "1", "Check")
    make_property_setter("Sales Order", "set_warehouse", "hidden", "1", "Check")
    make_property_setter("Sales Order", "total", "hidden", "1", "Check")
    make_property_setter("Sales Order", "section_break_48", "hidden", "1", "Check")
    make_property_setter("Sales Order", "section_break_40", "hidden", "1", "Check")
    make_property_setter("Sales Order", "section_break_43", "hidden", "1", "Check")
    make_property_setter("Sales Order", "terms_section_break", "hidden", "1", "Check")
    make_property_setter("Sales Order", "grand_total", "hidden", "1", "Check")
    make_property_setter("Sales Order", "disable_rounded_total", "hidden", "1", "Data")
    make_property_setter("Sales Order", "totals", "label", "Totals", "Data")
    make_property_setter("Sales Order", "payment_schedule_section", "hidden", "1", "Check")
    make_property_setter("Sales Order", "terms_section_break", "1", "hidden", "Check")
    make_property_setter("Sales Order", "currency_and_price_list", "1", "hidden", "Check")
    make_property_setter("Sales Order", "packing_list", "1", "hidden", "Check")
    make_property_setter("Sales Order", "currency_and_price_list", "hidden", "1", "Check")
    make_property_setter("Sales Order", "accounting_dimensions_section", "hidden", "1", "Column Break")
    make_property_setter("Sales Order", "posa_additional_notes_section", "hidden", "1", "Column Break")
    make_property_setter("Sales Order", "total_net_weight", "hidden", "1", "Float")
    make_property_setter("Sales Order", "rounding_adjustment", "hidden", "1", "Currency")
    make_property_setter("Sales Order", "cost_center", "default", "Main - SKSS", "Link")
   




   
