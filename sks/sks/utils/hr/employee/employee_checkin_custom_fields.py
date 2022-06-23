from xml.dom.pulldom import parseString
import frappe

def employee_checkin_customisation():
    create_employee_checkin_property_setter()
    create_custom_fields()


def create_employee_checkin_property_setter():
    employee_checkin=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee Checkin",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"skip_auto_attendance",
        "value":1
    })
    employee_checkin.save(ignore_permissions=True)

def create_custom_fields():
    pass