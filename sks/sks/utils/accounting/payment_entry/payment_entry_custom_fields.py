from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def payment_entry_customization():
    payment_entry_custom_fields()
    payment_entry_property_setter()

def payment_entry_custom_fields():
    custom_fields = {
        "Payment Entry":[
            dict(
                fieldname="driver",
                fieldtype="Link",
                label="Driver",
                insert_after="column_break_11",
                options ="Driver",
                read_only=1
            ),
            dict(
                fieldname="mode_of_payment_by_driver",
                fieldtype="Data",
                label="Mode of Payment By Driver",
                insert_after="driver",
                depends_on ="eval:doc.driver",
                read_only=1
            )
        ]
    }
    create_custom_fields(custom_fields)
    

def payment_entry_property_setter():
    pass
