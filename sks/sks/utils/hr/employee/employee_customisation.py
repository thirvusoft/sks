import frappe 

from sks.sks.utils.hr.employee.employee_checkin_custom_fields import create_employee_checkin_property_setter
from sks.sks.utils.hr.employee.employee_custom_fields import create_employee_property_setter

def employee_customisation():
    create_employee_checkin_property_setter()
    create_employee_property_setter()