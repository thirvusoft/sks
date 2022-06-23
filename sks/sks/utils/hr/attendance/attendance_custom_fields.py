import frappe

def attendance_customisation():
    attendance_property_setter()
    create_custom_fields()

    
def attendance_property_setter():
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

def create_custom_fields():
    pass