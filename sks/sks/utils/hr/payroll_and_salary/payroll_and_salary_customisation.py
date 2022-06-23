import frappe
 
from sks.sks.utils.hr.payroll_and_salary.payroll_entry.payroll_entry_custom_fields import create_payroll_entry_property_setter
from sks.sks.utils.hr.payroll_and_salary.salary_slip.salary_slip_custom_fields import create_salary_slip_property_setter
from sks.sks.utils.hr.payroll_and_salary.salary_structure.salary_structure_custom_fields import create_salary_structure_property_setter

def payroll_salary_customisation():
    create_payroll_entry_property_setter()
    create_salary_slip_property_setter()
    create_salary_structure_property_setter()