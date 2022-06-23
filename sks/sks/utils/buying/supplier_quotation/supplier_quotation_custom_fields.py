from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from sks.sks.utils.buying.supplier_quotation.supplier_quotation_item.supplier_quotation_item_custom_fields import supplier_quotation_item_customization
def supplier_quotation_customization():
    supplier_quotation_custom_fields()
    supplier_quotation_property_setter()
    supplier_quotation_item_customization()
def supplier_quotation_custom_fields():
    pass
def supplier_quotation_property_setter():                
        make_property_setter("Supplier Quotation", "terms", "hidden", 1,"Check")
        make_property_setter("Supplier Quotation", "more_info", "hidden", 1,"Check")
        make_property_setter("Supplier Quotation", "printing_settings", "hidden", 1,"Check")
