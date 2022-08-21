import frappe
@frappe.whitelist()
def batch_needed(doc,event):
    if doc.is_closing_shift_stock ==1:
        doc.has_batch_no=0
    else:
        doc.has_batch_no=1

def single_batch_validation(doc,event):
    if doc.is_single_batch:
        single_batch_verification = len(frappe.get_list("Batch",{"item":doc.item_code},pluck="name"))
        if single_batch_verification > 1:
            frappe.throw(frappe._(f"Already item :{doc.item_code} have {single_batch_verification} batches"))
        else:
            doc.create_new_batch=0