from sks.sks.utils.buying.purchase_invoice.purchase_invoice_item.purchase_invoice_item_custom_fields import purchase_invoice_item_custom_fields
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_invoice_customization():
          purchase_invoice_item_custom_fields()
          purchase_invoice_property_setter()
     
def purchase_invoice_property_setter():            
          make_property_setter("Sales Invoice", "party_account_currency", "hidden", "1", "Link")
          make_property_setter("Sales Invoice", "subscription_section", "hidden", "1", "Section Break")
          make_property_setter("Sales Invoice", "accounting_dimensions_section", "hidden", "1", "Section Break")
          make_property_setter("Sales Invoice", "supplier_invoice_details", "hidden", "1", "Section Break")
          make_property_setter("Sales Invoice", "update_stock", "hidden", "1", "Check")
          make_property_setter("Sales Invoice", "scan_barcode", "hidden", "1", "Data")
          make_property_setter("Sales Invoice", "terms_section_break", "hidden", "1", "Section Break")
          make_property_setter("Sales Invoice", "more_info", "hidden", "1", "Section Break")
          make_property_setter("Sales Invoice", "accounting_details_section", "hidden", "1", "Section Break")