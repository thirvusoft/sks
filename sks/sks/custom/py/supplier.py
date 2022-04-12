import frappe
import erpnext
from erpnext.regional.india.utils import validate_gstin_check_digit
from frappe.contacts.doctype.address.address import get_address_display

import re
from frappe import _

GSTIN_FORMAT = re.compile("^[0-9]{2}[A-Z]{4}[0-9A-Z]{1}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[1-9A-Z]{1}[0-9A-Z]{1}$")
GSTIN_UIN_FORMAT = re.compile("^[0-9]{4}[A-Z]{3}[0-9]{5}[0-9A-Z]{3}")
PAN_NUMBER_FORMAT = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")


def validate_gstin(doc,action):
	if not (doc.supplier_type == "Individual" or doc.gst_category == "Unregistered"):
		if doc.gstin:
			doc.gstin = doc.gstin.upper().strip()
		if len(doc.gstin) != 15:
			frappe.throw(_("A GSTIN must have 15 characters."), title=_("Invalid GSTIN"))

		if doc.gst_category and doc.gst_category == 'UIN Holders':
			if not GSTIN_UIN_FORMAT.match(doc.gstin):
				frappe.throw(_("The input you've entered doesn't match the GSTIN format for UIN Holders or Non-Resident OIDAR Service Providers"),
					title=_("Invalid GSTIN"))
		else:
			if not GSTIN_FORMAT.match(doc.gstin):
				frappe.throw(_("The input you've entered doesn't match the format of GSTIN."), title=_("Invalid GSTIN"))

			validate_gstin_check_digit(doc.gstin)

def create_address(doc):
	if doc.supplier_name != "NULL" :	
		if not frappe.db.get_value("Address",{'address_title' : 'supplier_name'}):
			addr = frappe.new_doc("Address")
			if doc.name:
				addr.append("links", {
					"link_doctype" : doc.doctype,
					"link_name": doc.name
				})
			addr.address_title = doc.supplier_name
			addr.address_line1 = doc.address_line_1
			addr.address_line2 = doc.address_line_2
			addr.gstin =doc.gstin
			addr.gst_state =doc.state
			addr.city = doc.city
			addr.state = doc.state
			addr.pincode = doc.pin_code
			addr.save()
		else:
			return
	if doc.is_primary_address == 1:
		frappe.db.set_value('Supplier',doc.name, 'supplier_primary_address',addr.name)
		frappe.db.set_value('Supplier',doc.name, 'primary_address',get_address_display(addr.name))