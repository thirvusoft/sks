import frappe


def create_salary_structure_property_setter():
    salary_structure=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Structure",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"letter_head",
        "value":1
    })
    salary_structure.save(ignore_permissions=True) 

    salary_structure=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Structure",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"time_sheet_earning_detail",
        "value":1
    })
    salary_structure.save(ignore_permissions=True) 

    salary_structure=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Structure",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"account",
        "value":1
    })
    salary_structure.save(ignore_permissions=True)

    salary_structure_assignment=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Structure",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"income_tax_slab",
        "value":1
    })
    salary_structure_assignment.save(ignore_permissions=True)

    salary_structure_assignment=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Structure",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"payroll_payable_account",
        "value":1
    })
    salary_structure_assignment.save(ignore_permissions=True)