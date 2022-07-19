import frappe
def create_penalty(doc,event):
    if doc.late_entry == 1:
        penalty_doc = frappe.new_doc('Employee Penalty')
        penalty_doc.employee = doc.employee
        penalty_doc.employee_name = doc.employee_name
        penalty_doc.posting_date = doc.attendance_date
        if frappe.db.exists('Penalty Reason', 'Late Entry'):
            penalty_doc.reason = 'Late Entry'
        else:
            reason_doc = frappe.new_doc('Penalty Reason')
            reason_doc.reason = 'Late Entry'
            reason_doc.save()
        
        if frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_amount"):
            penalty_doc.amount = frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_amount")
        penalty_doc.reference_doctype = doc.doctype
        penalty_doc.reference_document = doc.name
        penalty_doc.insert()
        penalty_doc.submit()
        frappe.db.commit()
        