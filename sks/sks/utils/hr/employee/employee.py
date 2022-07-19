from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def employee_custom_fields():
    custom_fields = {
        "Employee":[
            dict(
                fieldname="father_name",
                fieldtype="Data",
                label="Father Name",
                insert_after="blood_group",
              
            ),
            dict(
                fieldname="age",
                fieldtype="Data",
                label="Age",
                insert_after="date_of_birth",
                read_only=1
              
            ),
            dict(
                fieldname="mother_name",
                fieldtype="Data",
                label="Mother Name",
                insert_after="father_name",
              
            ),
            dict(fieldname='pos_neg_table', label='Positive Negative Feedback',
				fieldtype='Section Break',insert_after='education'),

            dict(fieldname='pos_table', label='Positive Negative Feedback',
            fieldtype='Table', options='Postive Negative Feedback',insert_after='pos_neg_table'),

            dict(fieldname='certificate_table', label='Certificate Deatils',
            fieldtype='Section Break',insert_after='pos_table'),

            dict(fieldname='certificate_deatils_table', label='Certificate Details',
            fieldtype='Table', options='Certificate Details',insert_after='certificate_table')

            
        ]
    }
    create_custom_fields(custom_fields)