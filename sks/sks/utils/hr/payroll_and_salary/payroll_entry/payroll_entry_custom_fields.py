import frappe

def payroll_entry_customisation():
    create_payroll_entry_property_setter()
    create_custom_fields()


def create_payroll_entry_property_setter():
    payroll_entry=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Payroll Entry",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"branch",
        "value":1
    })
    payroll_entry.save(ignore_permissions=True)

    payroll_entry=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Payroll Entry",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"salary_slip_based_on_timesheet",
        "value":1
    })
    payroll_entry.save(ignore_permissions=True) 

    payroll_entry=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Payroll Entry",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"accounting_dimensions_section",
        "value":1
    })
    payroll_entry.save(ignore_permissions=True)

    payroll_entry=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Payroll Entry",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"account",
        "value":1
    })
    payroll_entry.save(ignore_permissions=True)

    payroll_entry=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Payroll Entry",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"deduct_tax_for_unclaimed_employee_benefits",
        "value":1
    })
    payroll_entry.save(ignore_permissions=True)

    payroll_entry=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Payroll Entry",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"deduct_tax_for_unsubmitted_tax_exemption_proof",
        "value":1
    })
    payroll_entry.save(ignore_permissions=True) 


def create_custom_fields():
    pass