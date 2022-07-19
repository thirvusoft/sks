# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

# import frappe
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
			if frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_component"):
				additional_salary.salary_component = frappe.db.get_single_value("Thirvu HR Settings", "leave_penalty_component")
			additional_salary.amount = self.amount
			additional_salary.overwrite_salary_structure_amount = 0
			additional_salary.save()
			additional_salary.submit()
			frappe.db.commit()
		# else:

