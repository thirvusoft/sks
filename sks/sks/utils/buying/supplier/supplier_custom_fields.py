from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def supplier_customization():
    supplier_custom_fields()
    supplier_property_setter()
def supplier_custom_fields():
    custom_fields = {
        "Supplier": [
            dict(
                fieldname="gstin",
                fieldtype="Data",
                label="GSTIN",
                insert_after="default_bank_account",
                fetch_from="supplier_primary_address.gstin"
            )
            ]    
    }
    create_custom_fields(custom_fields)
def supplier_property_setter():                
    make_property_setter("Supplier", "tax_id", "hidden", 1,"Check")
    make_property_setter("Supplier", "warn_rfqs", "hidden", 1,"Check")
    make_property_setter("Supplier", "warn_pos", "hidden", 1,"Check")
    make_property_setter("Supplier", "prevent_rfqs", "hidden", 1,"Check")
    make_property_setter("Supplier", "prevent_pos", "hidden", 1,"Check")
    make_property_setter("Supplier", "website", "hidden", 1,"Check")
    make_property_setter("Supplier", "language", "hidden", 1,"Check")
    make_property_setter("Supplier", "is_frozen", "hidden", 1,"Check")
    make_property_setter("Supplier", "section_break_7", "hidden", 1,"Check")
    make_property_setter("Supplier", "country", "hidden", 1,"Check")
    make_property_setter("Supplier", "mobile_no", "unique", "1", "Check")
    make_property_setter("Supplier", "supplier_group", "default", "All Supplier Groups", "Link")
    make_property_setter("Supplier", "supplier_type", "default", "Company", "Select")
    make_property_setter("Supplier", "gst_category", "default", "Unregistered", "Select")
    make_property_setter("Supplier", "tax_category", "default", "In-State", "Link")