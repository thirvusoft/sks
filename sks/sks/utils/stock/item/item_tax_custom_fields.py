from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_tax_customization():
    item_tax_custom_fields()
    item_tax_property_setter()

def item_tax_custom_fields():
    pass
def item_tax_property_setter():
    # make_property_setter("Item Tax","tax_category","reqd","1","Check")
    pass


