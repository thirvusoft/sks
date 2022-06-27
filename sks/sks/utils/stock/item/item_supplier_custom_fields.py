from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_supplier_customization():
    item_supplier_custom_fields()
    item_supplier_property_setter()

def item_supplier_custom_fields():
    pass

def item_supplier_property_setter():
    make_property_setter("Item Supplier", "supplier_part_no", "hidden", 1, "Data")  