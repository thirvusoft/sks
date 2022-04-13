import frappe
import erpnext
from frappe import _
def validate_phone(doc,action):
   phone = doc.phone
   if phone:
       if not phone.isdigit() or len(phone) != 10:
           frappe.throw(frappe._("{0} is not a valid Phone Number.").format(phone), frappe.InvalidPhoneNumberError)
   mobile_no=doc.mobile_no
   if mobile_no:
       if not mobile_no.isdigit() or len(mobile_no) !=10:
           frappe.throw(frappe._("{0} is not a valid Mobile Number.").format(mobile_no), frappe.InvalidPhoneNumberError)