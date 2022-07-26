from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_customization():
    item_custom_fields()
    item_property_setter()
def item_custom_fields():
    custom_fields = {
        "Item": [
            dict(
                fieldname="is_expiry_item",
                fieldtype="Check",
                label="Is Expiry Item",
                insert_after="is_stock_item",
                hidden=0
            ),
            dict(
                fieldname="section_break_27",
                fieldtype="Section Break",
                label="Warehouse",
                insert_after="product_type",
                hidden=1
            ),
            dict(
                fieldname="column_break_29",
                fieldtype="Column Break",
                insert_after="rack",
            ),
            dict(
                fieldname="column_break_31",
                fieldtype="Column Break",
                insert_after="row",
            ),
            dict(
                fieldname="item_name_tamil",
                fieldtype="Data",
                label="\u0baa\u0bc6\u0bbe\u0bb0\u0bc1\u0bb3\u0bbf\u0ba9\u0bcd \u0baa\u0bc6\u0baf\u0bb0\u0bcd",
                insert_after="item_name",
                reqd=1,
                bold=1,
            ),
            dict(
                fieldname="product_type",
                fieldtype="Select",
                label="Product Type",
                insert_after="over_billing_allowance",
                options="\nEatable\nNon Eatable"
            ),
            dict(
                fieldname="mrp",
                fieldtype="Currency",
                label="MRP",
                insert_after="standard_rate",
            ),
            dict(
                fieldname="ts_supplier_items",
                fieldtype="Section Break",
                label="Supplier Items",
                insert_after="column_break2",
                depends_on="eval:!doc.is_fixed_asset",
            ),
            dict(
                fieldname="ts_markup_and_markdown",
                fieldtype="Section Break",
                label="Markup and Markdown",
                insert_after="image",
                hidden=0
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
            dict(
                label="Buying Margin",
                fieldname="buying_margin_sec_break",
                fieldtype="Section Break",
                insert_after="ts_markdown_price",
            ),
            dict(
                fieldname="ts_buying_margin",
                fieldtype="Select",
                label=" ",
                options="\nCustom",
                insert_after="buying_margin_sec_break",
                allow_in_quick_entry=1,
            ),
            dict(
                fieldname="ts_column_break_purchase_margin",
                fieldtype="Column Break",
                label="",
                insert_after="ts_buying_margin",
            ),
            dict(
                fieldname="warehouse_details",
                fieldtype="Section Break",
                label="Warehouse Details",
                insert_after="barcodes",
            ),
            dict(
                fieldname="warehouse",
                fieldtype="Table",
                label="Warehouse",
                options="Item Warehouse",
                insert_after="warehouse_details",
            ),
            dict(
                fieldname="buying_margin_percentage",
                fieldtype="Percent",
                label="Buying Margin Percentage",
                depends_on="eval:doc.ts_buying_margin==\"Custom\"",
                mandatory_depends_on="eval:doc.ts_buying_margin==\"Custom\"",
                insert_after="ts_column_break_purchase_margin",
                allow_in_quick_entry=1,
            ),
        ],
            
    }
    create_custom_fields(custom_fields)
def item_property_setter():                
    make_property_setter("Item", "supplier_details", "hidden", 1, "Check")
    make_property_setter("Item", "supplier_details", "collapsible", 0, "Check")
    make_property_setter("Item", "column_break2", "hidden", 1, "Check")
    make_property_setter("Item", "delivered_by_supplier", "hidden", 1, "Check")
    make_property_setter("Item", "is_item_from_hub", "hidden", 1, "Check")
    make_property_setter("Item", "is_nil_exempt", "hidden", 1, "Check")
    make_property_setter("Item", "is_non_gst", "hidden", 1, "Check")
    make_property_setter("Item", "standard_rate", "hidden", 1, "Check")
    make_property_setter("Item", "is_fixed_asset", "hidden", 1, "Check")
    make_property_setter("Item", "valuation_rate", "hidden", 1, "Check")
    make_property_setter("Item", "barcodes", "hidden", 0, "Check")
    make_property_setter("Item", "inventory_section", "hidden", 1, "Check")
    make_property_setter("Item", "reorder_section", "hidden", 0, "Check")
    make_property_setter("Item", "serial_nos_and_batches", "hidden", 1, "Check")
    make_property_setter("Item", "reorder_section", "hidden", 1, "Check")
    make_property_setter("Item", "serial_nos_and_batches", "hidden", 0, "Check")
    make_property_setter("Item", "variants_section", "hidden", 1, "Check")
    make_property_setter("Item", "defaults", "hidden", 1, "Check")
    make_property_setter("Item", "include_item_in_manufacturing", "hidden", 1, "Check")
    make_property_setter("Item", "item_name", "reqd", 1, "Check")
    make_property_setter("Item", "image", "in_preview", 0, "Check")
    make_property_setter("Item", "image", "hidden", 1, "Check")
    make_property_setter("Item", "deferred_expense_section", "hidden", 1, "Check")
    make_property_setter("Item", "purchase_details", "hidden", 1, "Check")
    make_property_setter("Item", "customer_details", "hidden", 1, "Check")
    make_property_setter("Item", "deferred_revenue", "hidden", 1, "Check")
    make_property_setter("Item", "sales_details", "hidden", 1, "Check")
    make_property_setter("Item", "foreign_trade_details", "hidden", 1, "Check")
    make_property_setter("Item", "more_information_section", "hidden", 1, "Check")
    make_property_setter("Item", "hub_publishing_sb", "hidden", 1, "Check")
    make_property_setter("Item", "manufacturing", "hidden", 1, "Check")
    make_property_setter("Item", "inspection_criteria", "hidden", 1, "Check")
    make_property_setter("Item", "item_code", "reqd", 1, "Check")
    make_property_setter("Item", "item_code", "hidden", 0, "Check")
    make_property_setter("Item", "manufacturing", "collapsible_depends_on","is_stock_item", "Code")
    make_property_setter("Item", "default_discount_account", "hidden", 1, "Check")
    make_property_setter("Item", "over_delivery_receipt_allowance", "hidden", 1, "Float")
    make_property_setter("Item", "over_billing_allowance", "hidden", 1, "Float")
    make_property_setter("Item", "opening_stock", "hidden", 1, "Float"),
   
