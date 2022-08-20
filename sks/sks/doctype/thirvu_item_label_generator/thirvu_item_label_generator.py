# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model import document
from frappe.model.document import Document
def barcode_label(doc,event):
	if doc.barcode:
		doc.label_barcode = doc.barcode
	else:
		frappe.throw("Item may not have barcode")
class ThirvuItemLabelGenerator(Document):
	pass