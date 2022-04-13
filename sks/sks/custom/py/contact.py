import frappe
import erpnext
from frappe import _
def validate_phone(doc,action):
	for row in doc.phone_nos:
		print(row.phone, row.phone.isdigit(), len(row.phone))
		if not row.phone.isdigit() or len(row.phone) != 10:
			frappe.throw(frappe._("{0} is not a valid Phone Number.").format(row.phone), frappe.InvalidPhoneNumberError)
