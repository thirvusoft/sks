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
          ],
          }
          create_custom_fields(custom_fields)
def purchase_receipt_item_property_setter():
          make_property_setter("Purchase Receipt Item", "barcode", "Hidden", 1, "Check")
         