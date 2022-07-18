from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def employee_advance_custom_fields():
    custom_fields = {
        "Employee Advance":[
            dict(
                fieldname="outstanding_amount",
                fieldtype="Currency",
                label="Outstanding Amount",
                insert_after="pending_amount",
                reqd=1,
                read_only=0
              
            ),
             dict(
                fieldname="from_date",
                fieldtype="Date",
                label="From Date",
                insert_after="outstanding_amount",
                reqd=1,
              
            ),
             dict(
                fieldname="to_date",
                fieldtype="Date",
                label="To Dtae",
                insert_after="from_date",
                reqd=1,
              
            )
        ]
    }
    create_custom_fields(custom_fields)




    		