import frappe
import erpnext
from frappe import _
def validate_phone(doc,action):
   cell_number = doc.cell_number
   if cell_number:
       if not cell_number.isdigit() or len(cell_number) != 10:
           frappe.throw(frappe._("{0} is not a valid Mobile Number.").format(cell_number), frappe.InvalidPhoneNumberError)
   emergency_phone_number=doc.emergency_phone_number
   if emergency_phone_number:
             if not emergency_phone_number.isdigit() or len(emergency_phone_number) != 10:
                    frappe.throw(frappe._("{0} is not a valid Emergency Phone Number." ).format(emergency_phone_number),)