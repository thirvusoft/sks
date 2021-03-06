# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ThirvuEmployeePenalty(Document):
	def before_save(self):
		if self.reason == 'Late Entry':
			if frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_amount"):
				self.amount = frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_amount")
	def on_submit(self):
		if not frappe.db.exists("Additional Salary", {"ref_docname": self.name}):
			additional_salary = frappe.new_doc('Additional Salary')
			additional_salary.ref_docname = self.name
			additional_salary.ref_doctype = self.doctype
			additional_salary.payroll_date = self.posting_date
			additional_salary.employee = self.employee
			additional_salary.salary_component = frappe.db.get_value("Thirvu Penalty Reason",self.reason,'salary_component')
			additional_salary.amount = self.amount
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
			additional_salary.ref_docname = self.name
			additional_salary.ref_doctype = self.doctype
			additional_salary.payroll_date = self.posting_date
			additional_salary.employee = self.employee
			additional_salary.salary_component = frappe.db.get_value("Thirvu Penalty Reason",self.reason,'salary_component')
			additional_salary.amount = self.amount
			additional_salary.overwrite_salary_structure_amount = 0
			additional_salary.save()
			additional_salary.submit()
			frappe.db.commit()
			frappe.db.commit()

