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
        ]
    }
    create_custom_fields(custom_fields)
    property_setter()