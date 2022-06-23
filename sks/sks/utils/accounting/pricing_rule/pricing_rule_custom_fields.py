from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def pricing_rule_customization():
    pricing_rule_custom_fields()
    pricing_rule_property_setter()

def pricing_rule_custom_fields():
    pass

def pricing_rule_property_setter():
    make_property_setter("Pricing Rule", "section_break_13", "hidden", "1", "Section Break")