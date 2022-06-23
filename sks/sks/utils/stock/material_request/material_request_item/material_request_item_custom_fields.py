from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def material_request_item_customization():
    materaial_request_item_custom_fields()
    materaial_request_item_property_setter()
def materaial_request_item_custom_fields():
    pass
def materaial_request_item_property_setter():
    make_property_setter("Material Request Item", "is_nil_exempt", "hidden", "1", "Check")
    make_property_setter("Material Request Item", "is_non_gst", "hidden", "1", "Check")
    make_property_setter("Material Request Item", "section_break_46", "hidden", "1", "Section Break")
    make_property_setter("Material Request Item", "manufacture_details", "hidden", "1", "Section Break")
    make_property_setter("Material Request Item", "more_info", "hidden", "1", "Section Break")