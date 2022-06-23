from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def driver_customization():
    driver_custom_fields()
    driver_property_setter()

def driver_custom_fields():
    custom_fields = {
        "Driver":[
            dict(
                fieldname="user_id",
                fieldtype="Link",
                label="User Id",
                insert_after="address",
                options ="User"
            ),
        ]
    }
    create_custom_fields(custom_fields)

def driver_property_setter():
    pass