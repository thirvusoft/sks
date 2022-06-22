import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def customer_customization():
          customer_order_custom_field()
          customer_order_custom_field()
def customer_order_custom_field():      
          custom_fields = {
                    
          }
          create_custom_fields(custom_fields)
def customer_order_property_setter():                
          # make_property_setter("Purchase Order", "item_price_changed", "Hidden", 1, "Check")
         pass