from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def supplier_quotation_item_customization():
    supplier_quotation_item_custom_fields()
    supplier_quotation_item_property_setter()
def supplier_quotation_item_custom_fields():
    pass
def supplier_quotation_item_property_setter():
    make_property_setter("Supplier Quotation Item", "ad_sec_break", "hidden", 1,"Check")
    make_property_setter("Supplier Quotation Item", "manufacture_details", "hidden", 1,"Check")