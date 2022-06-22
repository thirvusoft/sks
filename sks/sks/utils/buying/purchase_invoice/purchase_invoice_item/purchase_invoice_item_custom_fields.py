import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_invoice_item_custom_fields():
          custom_fields = {
          "Purchase Invoice Item":[
                    dict(
                              fieldname='ts_mrp', 
                              label='MRP',reqd=1,
                              fieldtype='Currency', 
                              insert_after='sec_break2',
                              read_only=1,
                              in_list_view=1,columns=2,
                              fetch_from="Purchase Receipt.ts_mrp and Purchase Order.ts_mrp"),
          ],
          }
          create_custom_fields(custom_fields)
