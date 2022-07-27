import frappe
@frappe.whitelist()
def batch_needed(doc,event):
    if doc.is_closing_shift_stock ==1:
        doc.has_batch_no=0
    else:
        doc.has_batch_no=1
