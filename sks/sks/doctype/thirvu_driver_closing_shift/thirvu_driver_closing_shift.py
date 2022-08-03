# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe,json
from frappe import _
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
				row.update({'mode_of_payment':data['mode_of_payment'],'amount':data['closing_amount'],'debit_account_head':account.accounts[0].default_account})
				table.append(row)
	except:
		pass
	return table


@frappe.whitelist()
def create_journal_entry(data,doc):
	data = json.loads(data)
	doc = json.loads(doc)

	new_jv_doc=frappe.new_doc('Journal Entry')
	new_jv_doc.voucher_type='Journal Entry'
	new_jv_doc.posting_date=doc['posting_date']
	new_jv_doc.company = doc['company']
	new_jv_doc.user_remark = _("POS Closing Shift for {0} to {1}").format(
				doc['period_start_date'], doc['period_end_date']
			)

	for value in range(0,len(data['account_details']),1):
		new_jv_doc.append('accounts',{'account':data['account_details'][value]['debit_account_head'],'credit_in_account_currency':data['account_details'][value]['amount']})
		new_jv_doc.append('accounts',{'account':data['account_details'][value]['credit_account_head'],'debit_in_account_currency':data['account_details'][value]['amount']})
		

	new_jv_doc.insert()
	new_jv_doc.submit()
	return 1