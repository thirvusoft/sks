import frappe

def create_employee_property_setter():
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"last_name",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"middle_name",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"salutation",
        "value":1
    })
    employee.save(ignore_permissions=True) 

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"grade",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"branch",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"employment_type",
        "value":1
    })
    employee.save(ignore_permissions=True)
    
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"reports_to",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"default_shift",
        "value":1
    })
    employee.save(ignore_permissions=True) 

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"employment_details",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"approvers_section",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"salary_information",
        "value":1
    })
    employee.save(ignore_permissions=True) 

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"health_insurance_section",
        "value":1
    })
    employee.save(ignore_permissions=True)
    
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"sb53",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"label",
        'property_type':"Section Break",
        'field_name':"erpnext_user",
        "value":"Thirvu User"
    })
    employee.save(ignore_permissions=True)