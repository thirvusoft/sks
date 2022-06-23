from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def supplier_customization():
    supplier_fields()
    supplier_property_setter()
def supplier_fields():
    custom_fields = {
        "Supplier": [
            dict(
                fieldname="gstin",
                fieldtype="Data",
                label="GSTIN",
                insert_after="default_bank_account",
                fetch_from="supplier_primary_address.gstin"
            ),
            ],      
    }
    create_custom_fields(custom_fields)
def supplier_property_setter():                
        make_property_setter("Supplier", "tax_id", "hidden", 1,"Check")
        make_property_setter("Supplier", "column_break2", "hidden", 1,"Check")