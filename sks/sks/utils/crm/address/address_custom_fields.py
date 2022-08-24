from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def address_customization():
    address_custom_field()
    address_property_setter()
     
def address_custom_field():
    custom_fields={
        "Address":[
            dict(fieldname='phone_2',
                label='Phone 2',
                fieldtype='Data',
                insert_after='phone',
            ),
        ]
    }
    create_custom_fields(custom_fields)

def address_property_setter(): 
    make_property_setter("Address", "links", "hidden", "1", "Check")