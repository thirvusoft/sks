import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def customer_feedback_form_customization():
          customer_feedback_form_property_setter()
def customer_feedback_form_property_setter():                
          make_property_setter("Customer Feedback Form", "customer_name", "reqd", 1, "Check")
         