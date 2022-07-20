import frappe, json
import erpnext
from frappe import _
from datetime import timedelta,datetime
from sks.sks.custom.py.default import validate_contact
from datetime import datetime 
from frappe.utils import getdate , get_date_str


def validate_phone(doc,action):
          validate_contact(doc.cell_number)
          validate_contact(doc.emergency_phone_number)

@frappe.whitelist()
def property_deduction(doc):
    doc = json.loads(doc)
    amount = 0
    date_format = '%Y-%m-%d'
    if not frappe.db.exists("Additional Salary", {"ref_docname": doc['name']}):
        additional_salary = frappe.new_doc('Additional Salary')
        additional_salary.ref_docname = doc['name']
        additional_salary.ref_doctype = doc['doctype']
        additional_salary.payroll_date = datetime.strptime(doc['relieving_date'],date_format) - timedelta(1)
        additional_salary.employee = doc['name']
        if frappe.db.get_single_value("Thirvu HR Settings", "property_reduction_component"):
            additional_salary.salary_component = frappe.db.get_single_value("Thirvu HR Settings", "property_reduction_component")
        for data in doc['ts_property_details']:
            amount += data['amount'] * data['count']
        additional_salary.amount = amount
        additional_salary.overwrite_salary_structure_amount = 0
        additional_salary.save()
        additional_salary.submit()
        frappe.db.commit()

    else:
        old = frappe.get_doc('Additional Salary',{'ref_docname':doc['name']})
        old.cancel()
        additional_salary = frappe.copy_doc(old) 
        additional_salary.amended_from = old.name 
        additional_salary.status = "Draft" 
        additional_salary.insert()
        additional_salary.ref_docname = doc['name']
        additional_salary.ref_doctype = doc['doctype']
        additional_salary.payroll_date = datetime.strptime(doc['relieving_date'],date_format) - timedelta(1)
        additional_salary.employee = doc['name']
        if frappe.db.get_single_value("Thirvu HR Settings", "property_reduction_component"):
            additional_salary.salary_component = frappe.db.get_single_value("Thirvu HR Settings", "property_reduction_component")
        for data in doc['ts_property_details']:
            amount += data['amount'] * data['count']
        additional_salary.amount = amount
        additional_salary.overwrite_salary_structure_amount = 0
        additional_salary.save()
        additional_salary.submit()
        frappe.db.commit()
def age_calculation(date_of_birth):

    date = getdate(date_of_birth)
    today = datetime.today()
    age = today.year - date.year 

    return age
