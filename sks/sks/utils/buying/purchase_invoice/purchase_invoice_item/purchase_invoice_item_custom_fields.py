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
                            dict(fieldname='ts_warehouse', label='TS Warehouse',
                fieldtype='Data', insert_after='warehouse',read_only=1)
          ],
          }
          create_custom_fields(custom_fields)

def purchase_invoice_item_property_setter():
    make_property_setter("Purchase Invoice Item", "is_nil_exempt", "hidden", "1", "Check")
    make_property_setter("Purchase Invoice Item", "is_non_gst", "hidden", "1", "Check")
    make_property_setter("Purchase Invoice Item", "section_break_82", "hidden", "1", "Section Break")
    make_property_setter("Purchase Invoice Item", "manufacture_details", "hidden", "1", "Section Break")
    make_property_setter("Purchase Invoice Item", "accounting", "hidden", "1", "Section Break")
    make_property_setter("Purchase Invoice Item", "deferred_expense_section", "hidden", "1", "Section Break")
    make_property_setter("Purchase Invoice Item", "reference", "hidden", "1", "Section Break")