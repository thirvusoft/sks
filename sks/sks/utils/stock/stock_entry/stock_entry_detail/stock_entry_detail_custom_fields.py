from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def stock_entry_detail_customization():
    stock_entry_detail_custom_fields()
    stock_entry_detail_property_setter()

def stock_entry_detail_custom_fields():
    custom_fields = {
        "Stock Entry Detail": [
            dict(
                fieldname="expiry_date",
                fieldtype="Date",
                label="Expiry Date",
                insert_after="item_code",
                mandatory_depends_on="eval:doc.t_warehouse",
            ),
        ],    
    }
    create_custom_fields(custom_fields)
    
def stock_entry_detail_property_setter():
    pass