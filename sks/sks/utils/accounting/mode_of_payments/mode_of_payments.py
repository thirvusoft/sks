import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def mode_of_payments():
    mode_of_payments_custom_fields()
    mode_of_payments_property_setter()

def mode_of_payments_custom_fields():
    custom_fields = {
        "Mode of Payment": [
            dict(
                fieldname="bank_type",
                fieldtype="Select",
                label="Bank Type",
                options="\nCard\nUPI",
                insert_after="type",
                depends_on="eval:doc.type==\"Bank\"",
            ),
        ]
    }
    create_custom_fields(custom_fields)
def mode_of_payments_property_setter():
    make_property_setter('Mode of Payment', 'type', 'options', "\nCash\nBank", 'Select')
