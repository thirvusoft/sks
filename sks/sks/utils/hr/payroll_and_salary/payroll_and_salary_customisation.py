import frappe
 
from sks.sks.utils.hr.payroll_and_salary.payroll_entry.payroll_entry_custom_fields import payroll_entry_customisation
from sks.sks.utils.hr.payroll_and_salary.salary_slip.salary_slip_custom_fields import salary_slip_customisation
from sks.sks.utils.hr.payroll_and_salary.salary_structure.salary_structure_custom_fields import salary_structure_customisation

def payroll_salary_customisation():
    payroll_entry_customisation()
    salary_slip_customisation()
    salary_structure_customisation()