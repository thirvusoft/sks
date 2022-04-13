import frappe
import erpnext
from frappe import _
def validate_phone(doc,action):
   phone = doc.phone
   if phone:
       if not phone.isdigit() or len(phone) != 10:
           frappe.throw(frappe._("{0} is not a valid Phone Number.").format(phone), frappe.InvalidPhoneNumberError)
 
