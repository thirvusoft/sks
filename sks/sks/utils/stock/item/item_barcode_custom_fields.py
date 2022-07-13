from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_barcode_customization():
    item_barcode_custom_fields()
    item_barcode_property_setter()

def item_barcode_custom_fields():
    pass
def item_barcode_property_setter():
    make_property_setter("Item Barcode", "barcode_type", "hidden", 1, "Check")
    make_property_setter("Item Barcode", "posa_uom", "hidden", 1, "Check")
    make_property_setter("Item Barcode", "barcode", "hidden", 0, "Check")
