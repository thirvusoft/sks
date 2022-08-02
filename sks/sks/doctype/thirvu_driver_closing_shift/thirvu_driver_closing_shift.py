# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document

class ThirvuDriverClosingShift(Document):
	pass
@frappe.whitelist()
def get_payment_details(doc):
	doc = json.loads(doc)
	table = []
	try:
		for data in doc['payment_reconciliation']:
			row = frappe._dict()
			account = frappe.get_doc('Mode of Payment',data['mode_of_payment'])
			if data['closing_amount']>0:
				print('ji')
				row.update({'mode_of_payment':data['mode_of_payment'],'amount':data['closing_amount'],'debit_account_head':account.accounts[0].default_account})
				table.append(row)
	except:
		pass
	print('hi')
	return table
