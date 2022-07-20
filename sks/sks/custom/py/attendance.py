import frappe
from datetime import datetime,timedelta

def create_penalty(doc,event):

    if doc.late_entry == 1:
        # start and end date
        datem = datetime.strptime(str(doc.attendance_date),"%Y-%m-%d")
        first_date = get_first_date_of_current_month(datem.year, datem.month)
        last_date = get_last_date_of_month(datem.year,datem.month)
        
        # count of late entry
        count = frappe.db.sql('''select count(name) from `tabAttendance` where employee = '{0}' and attendance_date between '{1}' and '{2}' and late_entry = '1' and docstatus = '1' '''.format(doc.employee,first_date,last_date),as_list=1)
        
        if count[0][0] > 3:
            penalty_doc = frappe.new_doc('Thirvu Employee Penalty')
            penalty_doc.employee = doc.employee
            penalty_doc.employee_name = doc.employee_name
            penalty_doc.posting_date = doc.attendance_date
            if frappe.db.exists('Thirvu Penalty Reason', 'Late Entry'):
                penalty_doc.reason = 'Late Entry'
            else:
                reason_doc = frappe.new_doc('Thirvu Penalty Reason')
                reason_doc.reason = 'Late Entry'
                reason_doc.save()
            
            if frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_amount"):
                penalty_doc.amount = frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_amount")
            penalty_doc.reference_doctype = doc.doctype
            penalty_doc.reference_document = doc.name
            penalty_doc.insert()
            penalty_doc.submit()
            frappe.db.commit()
            
def get_first_date_of_current_month(year, month):

    first_date = datetime(year, month, 1)
    return first_date.strftime("%Y-%m-%d")

def get_last_date_of_month(year, month):

    last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
    return last_date.strftime("%Y-%m-%d")
