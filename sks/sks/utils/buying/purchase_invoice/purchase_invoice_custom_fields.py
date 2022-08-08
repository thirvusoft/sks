from sks.sks.utils.buying.purchase_invoice.purchase_invoice_item.purchase_invoice_item_custom_fields import purchase_invoice_item_custom_fields, purchase_invoice_item_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_invoice_customization():
    purchase_invoice_item_custom_fields()
    purchase_invoice_item_property_setter()
    purchase_invoice_custom_field()
    purchase_invoice_property_setter()
     
def purchase_invoice_custom_field():
    pass

def purchase_invoice_property_setter(): 
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
    make_property_setter("Purchase Invoice", "cost_center", "default", "Main - SKS", "Link")
