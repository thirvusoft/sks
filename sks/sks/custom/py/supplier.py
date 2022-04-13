import frappe
import erpnext
from erpnext.regional.india.utils import validate_gstin_check_digit
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

