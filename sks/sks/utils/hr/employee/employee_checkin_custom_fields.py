import frappe

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