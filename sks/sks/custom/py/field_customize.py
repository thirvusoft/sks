import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from sks.sks.custom.py.property_setter import property_setter
def custom_fields():
    custom_fields = {
        "Sales Invoice": [
            dict(fieldname='time_of_delivery', label='Time of Delivery',
                fieldtype='Time', insert_after='delivery_status',hidden=1,allow_on_submit=1),
            dict(fieldname='delivery_status', label='Delivery Status',
                fieldtype='Select', insert_after='due_date',default="Ready To Dispatch",
                options="Attempt\nDelivered\nNot Delivered\nReady To Dispatch\nReattempt\nReturned"),
            dict(fieldname='reason', label='Reason',
                fieldtype='Data', insert_after='time_of_delivery', allow_on_submit=1),
            dict(fieldname='scan_barcode_to_verify_the_items', label='Scan Barcode To Verify The Items',
                fieldtype='Data', insert_after='scan_barcode',options="Barcode",hidden=1,),
            dict(fieldname='mode_of_delivery', label='Mode of Delivery',
                fieldtype='Data', insert_after='reason',fetch_from="Sales Order.mode_of_delivery",read_only=1,),
        ],
        "Sales Invoice Item":[
             dict(fieldname='item_verified', label='Item Verified',
                fieldtype='Check', insert_after='amount',read_only=1,in_list_view=1,columns=2),
        ],
        "Purchase Order": [
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
    property_setter()