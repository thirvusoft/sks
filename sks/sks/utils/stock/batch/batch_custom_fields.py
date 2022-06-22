from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def batch_customization():
    batch_custom_fields()
    batch_property_setter()
def batch_custom_fields():
    custom_fields = {
        "Batch": [
            dict(
                fieldname="barcode",
                fieldtype="Data",
                label="Barcode",
                insert_after="expiry_date"
            ),
            dict(
                fieldname="ts_mrp",
                fieldtype="Currency",
                label="MRP",
                insert_after="barcode"
            ),
            dict(
                fieldname="ts_selling_price",
                fieldtype="Currency",
                label="Selling Price",
                insert_after="posa_btach_price"
            ),
            dict(
                fieldname="ts_valuation_rate",
                fieldtype="Currency",
                label="Valuation Rate",
                insert_after="ts_mrp"
            ),
            ],      
    }
    create_custom_fields(custom_fields)
def batch_property_setter():                
          pass