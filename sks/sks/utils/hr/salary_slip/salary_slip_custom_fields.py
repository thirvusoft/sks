import frappe

def create_salary_slip_property_setter():
    salary_slip=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Slip",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"deduct_tax_for_unclaimed_employee_benefits",
        "value":1
    })
    salary_slip.save(ignore_permissions=True)

    salary_slip=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Slip",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"deduct_tax_for_unsubmitted_tax_exemption_proof",
        "value":1
    })
    salary_slip.save(ignore_permissions=True) 

    salary_slip=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Salary Slip",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"salary_slip_based_on_timesheet",
        "value":1
    })
    salary_slip.save(ignore_permissions=True)