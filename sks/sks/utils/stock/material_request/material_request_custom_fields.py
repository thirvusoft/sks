from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from sks.sks.utils.stock.material_request.material_request_item.material_request_item_custom_fields import material_request_item_customization
def material_request_customization():
    materaial_request_custom_fields()
    materaial_request_property_setter()
    material_request_item_customization()
def materaial_request_custom_fields():
    pass
def materaial_request_property_setter():
    make_property_setter("Material Request", "reference", "hidden", 1, "Check")
    make_property_setter("Material Request", "printing_details", "hidden", 1, "Check")
    make_property_setter("Material Request", "terms_section_break", "hidden", 1, "Check")
    make_property_setter("Material Request", "scan_barcode", "hidden", 0, "Check")