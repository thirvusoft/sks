import frappe
def workflow_document_creation():
    property_creator()
    create_state()
    create_action()
    create_rate_changer_from_purchase_order()

def create_rate_changer_from_purchase_order():
    if frappe.db.exists('Workflow', 'Rate Changer From Purchase Order'):
        frappe.delete_doc('Workflow', 'Rate Changer From Purchase Order')
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Rate Changer From Purchase Order'
    workflow.document_type = 'Purchase Receipt'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1
    workflow.append('states', dict(
        state = 'Draft', allow_edit = 'Purchase User',update_field = 'status', update_value = 'open'
    ))
    workflow.append('states', dict(
        state = 'Approval Pending', allow_edit = 'Purchase Manager',update_field = 'status', update_value = 'Approval Pending'
    ))
    workflow.append('states', dict(
        state = 'Approved', allow_edit = 'Purchase User',update_field = 'status', update_value = 'Approved'
    ))
    workflow.append('states', dict(
        state = 'Rejected', allow_edit = 'Purchase Manager',update_field = 'status', update_value = 'Rejected'
    ))
    workflow.append('states', dict(
        state = 'Submitted',doc_status=1, allow_edit = 'Purchase User',update_field = 'status', update_value = 'To Bill'
    ))
    workflow.append('states', dict(
        state = 'To Bill',doc_status=1, allow_edit = 'Purchase User',update_field = 'status', update_value = 'To Bill'
    ))
    
    workflow.append('transitions', dict(
        state = 'Draft', action='Send Approve Permission', next_state = 'Approval Pending',
        allowed='Purchase User', allow_self_approval= 1,condition="doc.ts_item_price_changed==1 or doc.ts_markup_and_markdown_variations == 1 or (doc.ts_item_price_changed==1 and doc.ts_markup_and_markdown_variations == 1)"
    ))
    workflow.append('transitions', dict(
        state = 'Approval Pending', action='Approve', next_state = 'Approved',
        allowed='Purchase Manager', allow_self_approval= 1,condition="doc.ts_item_price_changed==1 or doc.ts_markup_and_markdown_variations == 0 or (doc.ts_item_price_changed==0 and doc.ts_markup_and_markdown_variations == 0)"
    ))
    workflow.append('transitions', dict(
        state = 'Approval Pending', action='Reject', next_state = 'Rejected',
        allowed='Purchase Manager', allow_self_approval= 1,condition="doc.ts_item_price_changed==1 or doc.ts_markup_and_markdown_variations == 1 or (doc.ts_item_price_changed==1 and doc.ts_markup_and_markdown_variations == 1)"
    ))
    workflow.append('transitions', dict(
        state = 'Approved', action='Submit', next_state = 'To Bill',
        allowed='Purchase User', allow_self_approval= 1,condition="doc.ts_item_price_changed==1 or doc.ts_markup_and_markdown_variations == 0 or (doc.ts_item_price_changed==0 and doc.ts_markup_and_markdown_variations == 0)"
    ))
    workflow.append('transitions', dict(
        state = 'Draft', action='Submit', next_state = 'To Bill',
        allowed='Purchase User', allow_self_approval= 1,condition="doc.ts_item_price_changed==0 and doc.ts_markup_and_markdown_variations == 0"
    ))
    workflow.insert(ignore_permissions=True)
    return workflow
def create_state():
    list=["Draft","Approval Pending","Submitted","Rejected","Approved","To Bill"]
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            if(row=="Draft"):
                new_doc.style="Danger"
            if(row=="Approval Pending"):
                new_doc.style="Primary"
            if(row=="Rejected"):
                new_doc.style="Danger"
            if(row=="To Bill"):
                new_doc.style="Warning"
            if(row=="Approved"):
                new_doc.style="Success"
            new_doc.save()
def create_action():
    list=["Reject","Send Approve Permission","Approve","Submit","Approve"]
    for row in list:
        if not frappe.db.exists('Workflow Action Master', row):
            new_doc = frappe.new_doc('Workflow Action Master')
            new_doc.workflow_action_name = row
            new_doc.save()
def property_creator():
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
        'property':"label",
        'property_type':"Section Break",
        'field_name':"erpnext_user",
        "value":"Thirvu User"
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

    attendance=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Attendance",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"details_section",
        "value":1
    })
    attendance.save(ignore_permissions=True) 

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