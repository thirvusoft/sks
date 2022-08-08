from sks.sks.utils.buying.purchase_invoice.purchase_invoice_item.purchase_invoice_item_custom_fields import purchase_invoice_item_custom_fields, purchase_invoice_item_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_invoice_customization():
    purchase_invoice_item_custom_fields()
    purchase_invoice_item_property_setter()
    purchase_invoice_custom_field()
    purchase_invoice_property_setter()
     
def purchase_invoice_custom_field():
        custom_fields = {
                    "Purchase Invoice": [
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
                                        hidden=0
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
                              ),
                                dict(
                                        fieldname='to_verify_free_item_from_supplier', 
                                        label='To Verify Free Item From Supplier',
                                        fieldtype='Table', 
                                        options= "Supplier Free Item",
                                        insert_after='thirvu_items_to_verify',
                                        
                              ),
                              dict(
                                        fieldname='item_verified', 
                                        label='Supplier Free Item verified',
                                        fieldtype='Check', 
                                        insert_after='to_verify_free_item_from_supplier',
                                                  
                              ),
                              dict(
                                        fieldname='scanned_items', 
                                        label='Scanned items',
                                        fieldtype='Small Text', 
                                        insert_after='scan_barcode_to_verify_the_items',
                                        no_copy=1,
                                        hidden=1
                                                  
                              ),
                              dict(
                                        fieldname='scanned_barcodes', 
                                        label='Scanned Barcodes',
                                        fieldtype='Small Text', 
                                        insert_after='scanned_items',
                                        no_copy=1,
                                        hidden=1
                                                  
                              )
          
                    ],
            }
        create_custom_fields(custom_fields)

def purchase_invoice_property_setter():
    make_property_setter("Purchase Invoice", "scan_barcode", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "subscription_section", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "sec_warehouse", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "taxes_section", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "totals", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "disable_rounded_total", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "total_net_weight", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "project", "hidden", 1, "Check")
    
    make_property_setter("Purchase Invoice", "update_stock", "default", 1, "Small Text")
    make_property_setter("Purchase Invoice", "party_account_currency", "hidden", "1", "Check")
    make_property_setter("Purchase Invoice", "subscription_section", "hidden", "1", "Check")
    make_property_setter("Purchase Invoice", "accounting_dimensions_section", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "supplier_invoice_details", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "update_stock", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "scan_barcode", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "terms_section_break", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "more_info", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "accounting_details_section", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "printing_settings", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "gst_section", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "sb_14", "hidden", 1, "Check")
    # make_property_setter("Purchase Invoice", "tax_id", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "due_date", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "tax_withholding_category", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "apply_tds", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "currency_and_price_list", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "advances_section", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "rounding_adjustment", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "total_taxes_and_charges", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "taxes_and_charges_deducted", "hidden", 1, "Check")
    make_property_setter("Purchase Invoice", "is_subcontracted", "hidden", 1, "Check")
