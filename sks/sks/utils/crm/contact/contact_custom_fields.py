from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def contact_customization():
    contact_custom_field()
    contact_property_setter()
     
def contact_custom_field():
    pass

def contact_property_setter(): 
    make_property_setter("Contact", "more_info", "hidden", "1", "Check")
    make_property_setter("Contact", "department", "hidden", "1", "Check")
    make_property_setter("Contact", "unsubscribed", "hidden", "1", "Check")
   