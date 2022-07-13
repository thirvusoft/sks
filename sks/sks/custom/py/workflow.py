import frappe
def workflow_document_creation():
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
        state = 'Draft', action='Request Approve Permission', next_state = 'Approval Pending',
        allowed='Purchase User', allow_self_approval= 1,condition="doc.total_rejected_qty > 0 or doc.ts_item_price_changed == 1 or doc.ts_markup_and_markdown_variations == 1 or doc.thirvu_altered_quantity"
    ))
    workflow.append('transitions', dict(
        state = 'Approval Pending', action='Approve', next_state = 'Approved',
        allowed='Purchase Manager', allow_self_approval= 1,condition="doc.ts_markup_and_markdown_variations == 0 and (doc.check_qty == 1 or not doc.thirvu_altered_quantity)"
    ))
    workflow.append('transitions', dict(
        state = 'Approval Pending', action='Reject', next_state = 'Rejected',
        allowed='Purchase Manager', allow_self_approval= 1
    ))
    workflow.append('transitions', dict(
        state = 'Approved', action='Submit', next_state = 'To Bill',
        allowed='Purchase User', allow_self_approval= 1,condition="doc.ts_markup_and_markdown_variations == 0 and (doc.check_qty == 1 or not doc.thirvu_altered_quantity)"
    ))
    workflow.append('transitions', dict(
        state = 'Draft', action='Submit', next_state = 'To Bill',
        allowed='Purchase User', allow_self_approval= 1,condition="doc.total_rejected_qty == 0 and doc.ts_item_price_changed == 0 and doc.ts_markup_and_markdown_variations == 0 and not doc.thirvu_altered_quantity"
    ))
    workflow.append('transitions', dict(
        state = 'Approved', action='Reject', next_state = 'Rejected',
        allowed='Purchase Manager', allow_self_approval= 1
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
    list=["Reject","Request Approve Permission","Approve","Submit"]
    for row in list:
        if not frappe.db.exists('Workflow Action Master', row):
            new_doc = frappe.new_doc('Workflow Action Master')
            new_doc.workflow_action_name = row
            new_doc.save()