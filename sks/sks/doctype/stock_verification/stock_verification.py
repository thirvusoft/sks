# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class StockVerification(Document):
	pass


@frappe.whitelist()
def stock_emtry_creation(doc,event):
	if(doc.difference>0):
		stock_doc = frappe.new_doc('Stock Entry')
		items=[]
		items.append({
			't_warehouse':doc.item_warehouse,
			'item_code': doc.select_item,
			'qty':doc.difference,
			'batch_no':doc.batch_no
		})

		stock_doc.update({
			'stock_entry_type':"Material Receipt",
			'items':items,
			
		})
		stock_doc.insert()
		stock_doc.submit()
		frappe.db.commit()
		return stock_doc.name



