from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def packed_item_customization():
    packed_item_custom_field()
    packed_item_property_setter()
     
def packed_item_custom_field():
    pass

def packed_item_property_setter(): 
    make_property_setter("Packed Item", "rate", "read_only", "1", "Check")