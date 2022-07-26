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
            dict(
                fieldname="thirvu_mode_of_payments_SB",
                fieldtype="Section Break",
                insert_after="expiry_date",
            ),
            dict(
                fieldname="thirvu_mode_of_payments",
                fieldtype="Table",
                label="Mode of Payments",
                insert_after="thirvu_mode_of_payments_SB",
                options ="Thirvu Driver Mode of Payments",
                allow_on_submit=1
            )
        ]
    }
    create_custom_fields(custom_fields)

def driver_property_setter():
    make_property_setter("Driver","full_name","unique","Check",1)
