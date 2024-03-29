from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_price_customization():
    item_price_custom_fields()
    item_price_property_setter()

def item_price_custom_fields():
    custom_fields = {
        "Item Price": [
            dict(
                fieldname="ts_mrp",
                fieldtype="Currency",
                label="MRP",
                insert_after="price_list_rate",
                reqd=1
            ),
        ]
    }
    create_custom_fields(custom_fields)
def item_price_property_setter():
    make_property_setter("Item Price","packing_unit","hidden",1,"Check")
    make_property_setter("Item Price","lead_time_days","hidden",1,"Check")
    make_property_setter("Item Price","reference","hidden",1,"Check")
    make_property_setter("Item Price","note","hidden",1,"Check")