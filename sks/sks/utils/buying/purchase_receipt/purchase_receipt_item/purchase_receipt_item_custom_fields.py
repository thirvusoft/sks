import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_receipt_item_custom_fields():
          custom_fields = {
          "Purchase Receipt Item":[
                    dict(
                              fieldname='expiry_date', 
                              label='Expiry Date',
                              fieldtype='Date', 
                              insert_after='rejected_qty',
                              in_list_view=1,reqd=1
                    ),
                    dict(
                              fieldname='item_verified', 
                              label='Item Verified',
                              fieldtype='Check', 
                              insert_after='amount',
                              in_list_view=1,
                              read_only=1
                    ),
                    dict(
                              fieldname='ts_mrp', 
                              label='MRP',
                              fieldtype='Currency', 
                              insert_after='expiry_date',
                              in_list_view=1,
                              reqd=1
                    ),
                    dict(
                              fieldname='ts_selling_rate', 
                              label='Selling Rate',
                              fieldtype='Currency', 
                              insert_after='ts_mrp',
                              read_only=1
                    ),
                    dict(
                              fieldname='ts_valuation_rate', 
                              label='Valuation Rate',
                              fieldtype='Currency', 
                              insert_after='retain_sample', 
                              read_only=1
                    ),
                       dict(fieldname='ts_warehouse', label='TS Warehouse',
                fieldtype='Data', insert_after='warehouse')
          ],
          }
          create_custom_fields(custom_fields)
          
def purchase_receipt_item_property_setter():
    make_property_setter("Purchase Receipt Item", "is_nil_exempt", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "is_non_gst", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "section_break_80", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "manufacture_details", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "allow_zero_valuation_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "section_break_4", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "item_weight_details", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "accounting_details_section", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "accounting_details_section", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "bom", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "serial_no", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "rejected_serial_no", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "rate_and_amount", "hidden", 1, "Check")
    # make_property_setter("Purchase Receipt Item", "base_rate", "reqd", 1, "Check")
    # make_property_setter("Purchase Receipt Item", "base_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "base_amount", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "base_net_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "base_net_amount", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "landed_cost_voucher_amount", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "billed_amt", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "stock_uom_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt Item", "project", "hidden", 1, "Check")
         