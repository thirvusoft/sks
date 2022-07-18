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
            ),
            dict(
                fieldname="ts_markup_and_markdown",
                fieldtype="Section Break",
                label="Markup and Markdown",
                insert_after="prevent_pos",
            ),
            dict(
                fieldname="ts_column_break",
                fieldtype="Column Break",
                label="",
                insert_after="select_selling_price_type",
            ),
            dict(
                fieldname="ts_markup_price",
                fieldtype="Percent",
                label="Markup Percentage",
                depends_on="eval:doc.select_selling_price_type==\"Markup\"",
                mandatory_depends_on="eval:doc.select_selling_price_type==\"Markup\"",
                insert_after="ts_column_break",
                allow_in_quick_entry=1,
            ),
            dict(
                fieldname="ts_markdown_price",
                fieldtype="Percent",
                label="Markdown Percentage",
                depends_on="eval:doc.select_selling_price_type==\"Markdown\"",
                mandatory_depends_on="eval:doc.select_selling_price_type==\"Markdown\"",
                insert_after="ts_markup_price",
                allow_in_quick_entry=1,
            ),
            dict(
                fieldname="select_selling_price_type",
                fieldtype="Select",
                label="Select Selling Price Type",
                options="\nMarkup\nMarkdown",
                reqd=1,
                insert_after="ts_markup_and_markdown",
                allow_in_quick_entry=1,
            ),
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