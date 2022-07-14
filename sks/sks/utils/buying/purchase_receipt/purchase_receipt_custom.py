from sks.sks.utils.buying.purchase_receipt.purchase_receipt_item.purchase_receipt_item_custom_fields import purchase_receipt_item_custom_fields, purchase_receipt_item_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_receipt_customization():
          purchase_receipt_custom_field()
          purchase_receipt_property_setter()
          purchase_receipt_item_custom_fields()
          purchase_receipt_item_property_setter()
def purchase_receipt_custom_field(): 
          custom_fields = {
                    "Purchase Receipt": [
                              dict(
                                        fieldname='thirvu_items_to_verify', 
                                        label='Items To Verify for Markup / Markdown',
                                        fieldtype='Table', 
                                        insert_after='items',
                                        options="Thirvu Items To Verify",
                                        no_copy=1
                              ),
                              dict(
                                        fieldname='thirvu_altered_quantity', 
                                        label='Items To Verify for Altered Quantity',
                                        fieldtype='Table', 
                                        insert_after='thirvu_items_to_verify',
                                        options="TS Item Verification for Altered Quantity",
                                        no_copy=1
                              ),
                              dict(
                                        fieldname='thirvu_price_changed_items', 
                                        label='Price Changed Items',
                                        fieldtype='Table', 
                                        insert_after='check_qty',
                                        options="Thirvu Price Changed Items",
                                        no_copy=1
                              ),
                              dict(
                                        fieldname='check_qty', 
                                        label='Altered Item Quantity Verified',
                                        fieldtype='Check',
                                        insert_after='thirvu_altered_quantity',
                                        hidden=1
                              ),
                              dict(
                                        fieldname='ts_item_price_changed', 
                                        label='Item Price Changed',
                                        fieldtype='Check', 
                                        insert_after='check_qty',
                                        permlevel=2,hidden=1,
                                        read_only=1
                              ),
                              dict(
                                        fieldname='thirvu_item_price_changed', 
                                        label='Item Price Changes Verified',
                                        fieldtype='Check', 
                                        insert_after='thirvu_price_changed_items',
                              ),
                              dict(
                                        fieldname='ts_markup_and_markdown_variations', 
                                        label='TS Markup And Markdown Variations',
                                        fieldtype='Check', 
                                        insert_after='range', 
                                        read_only=1,
                                        no_copy=1,
                              ),
                              dict(
                                        fieldname='ts_markdown_items', 
                                        label='TS Markdown Items',
                                        fieldtype='Long Text', 
                                        insert_after='ts_markup_and_markdown_variations',
                                        read_only=1,
                                        no_copy=1,
                              ),
                              dict(
                                        fieldname='ts_markup_items', 
                                        label='TS Markup Items',
                                        fieldtype='Long Text', 
                                        insert_after='ts_markdown_items', 
                                        read_only=1,
                                        no_copy=1
                              ),
                              dict(
                                        fieldname='scan_barcode_to_verify_the_items', 
                                        label='Scan Barcode To Verify The Items',
                                        fieldtype='Data', 
                                        insert_after='scan_barcode',
                                        options="Barcode"
                              ),
                               dict(
                                        fieldname='total_rejected_qty', 
                                        label='Total Rejected Qty',
                                        fieldtype='Int', 
                                        insert_after='items',
                                        read_only=1
                              ),
                                dict(
                                        fieldname="is_approved",
                                        fieldtype='Check',
                                        label="Approved All Rejected Items",
                                        insert_after="total_rejected_qty",
                                        depends_on="eval:doc.total_rejected_qty>0 ||doc.workflow_state=='Approval Pending'",
                              )
                    ],
          }
          create_custom_fields(custom_fields)
def purchase_receipt_property_setter(): 
    make_property_setter("Purchase Receipt", "scan_barcode", "hidden", 1, "Check")
    make_property_setter("Purchase Receipt", "supplier_delivery_note", "hidden", 1, "Data")
    make_property_setter("Purchase Receipt", "raw_material_details", "hidden", 1, "Section Break")
    make_property_setter("Purchase Receipt", "transporter_info", "hidden", 1, "Section Break")
    make_property_setter("Purchase Receipt", "printing_settings", "hidden", 1, "Section Break")
    make_property_setter("Purchase Receipt", "subscription_detail", "hidden", 1, "Section Break")
    make_property_setter("Purchase Receipt", "more_info", "hidden", 1, "Section Break")
    make_property_setter("Purchase Receipt", "accounting_details_section", "hidden", 0, "Section Break")
    