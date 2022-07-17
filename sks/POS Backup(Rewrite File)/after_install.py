import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def customization():
    custom_field()
    property_setter()
def custom_field():
    custom_fields={
        "POS Opening Shift":[
            dict(fieldname='ts_pos_closing_shift_created',
                label='ts pos closing shift created',
                fieldtype='Check', 
                insert_after='section_break_9',
                hidden=1,
                allow_on_submit=1),
        ]
    }
    create_custom_fields(custom_fields)
    custom_fields={
        "POS Closing Shift":[
            dict(fieldname='ts_denomination_details',
                label='Denomination Details',
                fieldtype='Section Break', 
                insert_after='payment_reconciliation'),
            dict(fieldname='ts_denomination_counts',
                label=' ',
                fieldtype='Table', 
                insert_after='ts_denomination_details',
                options="Denomination",
                read_only=1),
            dict(fieldname='ts_denomination_total',
                label='Denomination Total',
                fieldtype='Currency', 
                insert_after='ts_denomination_counts',
                read_only=1),
            dict(fieldname='ts_column_break',
                label=' ',
                fieldtype='Column Break',
                insert_after='ts_denomination_total',),
        ]
    }
    create_custom_fields(custom_fields)

def property_setter():
    pass