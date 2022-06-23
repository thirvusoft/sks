import frappe 

from sks.sks.utils.hr.employee.employee_checkin_custom_fields import employee_checkin_customisation
from sks.sks.utils.hr.employee.employee_custom_fields import employee_customisations

def employee_customisation():
    employee_checkin_customisation()
    employee_customisations()