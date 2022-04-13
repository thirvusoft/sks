import frappe
import erpnext
from frappe import _

def validate_contact(contact_no):
   if contact_no:
       if not contact_no.isdigit() or len(contact_no) != 10:
           frappe.throw(frappe._("{0} is not a valid Phone Number.").format(contact_no), frappe.InvalidPhoneNumberError)