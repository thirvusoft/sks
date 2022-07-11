from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from sks.sks.utils.stock.stock_entry.stock_entry_detail.stock_entry_detail_custom_fields import stock_entry_detail_customization
def stock_entry_customization():
    stock_entry_custom_fields()
    stock_entry_property_setter()
    stock_entry_detail_customization()

def stock_entry_custom_fields():
    pass   
def stock_entry_property_setter():
    pass