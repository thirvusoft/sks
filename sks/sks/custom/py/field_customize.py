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
        "Purchase Receipt": [
            dict(fieldname='thirvu_items_to_verify', label='Items To Verify',
                fieldtype='Table', insert_after='items',options="Thirvu Items To Verify",no_copy=1),
            dict(fieldname='ts_item_price_changed', label='Item Price Changed',
                fieldtype='Check', insert_after='thirvu_items_to_verify',permlevel=2,hidden=1,read_only=1),
            dict(fieldname='ts_markup_and_markdown_variations', label='TS Markup And Markdown Variations',
                fieldtype='Check', insert_after='range', read_only=1,no_copy=1,),
            dict(fieldname='ts_markdown_items', label='TS Markdown Items',
                fieldtype='Long Text', insert_after='ts_markup_and_markdown_variations',read_only=1,no_copy=1,),
            dict(fieldname='ts_markup_items', label='TS Markup Items',
                fieldtype='Long Text', insert_after='ts_markdown_items', read_only=1,no_copy=1),
            dict(fieldname='column_break_47',fieldtype='Column Break',
                 insert_after='scan_barcode'),
            dict(fieldname='scan_barcode_to_verify_the_items', label='Scan Barcode To Verify The Items',
                fieldtype='Data', insert_after='column_break_47',options="Barcode"),
        ],
        "Purchase Receipt Item":[
            dict(fieldname='expiry_date', label='Expiry Date',
                fieldtype='Date', insert_after='rejected_qty'),
            dict(fieldname='item_verified', label='Item Verified',
                fieldtype='Check', insert_after='amount', read_only=1),
            dict(fieldname='ts_mrp', label='MRP',
                fieldtype='Currency', insert_after='expiry_date'),
            dict(fieldname='ts_selling_rate', label='Selling Rate',
                fieldtype='Currency', insert_after='ts_mrp',read_only=1),
            dict(fieldname='ts_valuation_rate', label='Valuation Rate',
                fieldtype='Currency', insert_after='retain_sample', read_only=1),
        ],
        "Purchase Invoice Item":[
           dict(fieldname='ts_mrp', label='MRP',reqd=1,
               fieldtype='Currency', insert_after='sec_break2',read_only=1,in_list_view=1,columns=2,fetch_from="Purchase Receipt.ts_mrp and Purchase Order.ts_mrp"),
       ] 
    }
    create_custom_fields(custom_fields)
    property_setter()