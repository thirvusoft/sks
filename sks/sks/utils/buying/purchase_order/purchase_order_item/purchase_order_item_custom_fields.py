import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def purchase_order_item_custom_fields():
          custom_fields = {
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
