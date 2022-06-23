from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def delivery_stop_customization():
    delivery_stop_custom_fields()
    delivery_stop_property_setter()
def delivery_stop_custom_fields():
    custom_fields = {
        "Delivery Stop": [
            dict(
                fieldname="sales_invoice",
                fieldtype="Link",
                label="Rack",
                insert_after="delivery_note",
                options="Sales Invoice"
            ),
            dict(
                fieldname="reason",
                fieldtype="Data",
                label="Reason",
                insert_after="mobile",
                in_preview=1,
                depends_on="// eval:in_list([\"Returned\",\"Reattempt\",\"Not Delivered\"],doc.delivery_status)",
                allow_on_submit=1
            ),
            dict(
                fieldname="time_of_delivery",
                fieldtype="Time",
                label="Time of Delivery",
                insert_after="reason",
                in_preview=1,
                depends_on="eval:doc.delivery_status == \"Delivered\"",
                allow_on_submit=1
            ),
            dict(
                fieldname="amount",
                fieldtype="Data",
                label="Amount",
                insert_after="time_of_delivery",
                in_preview=1,
                depends_on="eval:doc.delivery_status == \"Delivered\"",
                allow_on_submit=1
            ),
            dict(
                fieldname="delivery_status",
                fieldtype="Select",
                label="Delivery Status",
                insert_after="sales_invoice",
                in_preview=1,
                options="Attempt\nDelivered\nNot Delivered\nReady To Dispatch\nReattempt\nReturned",
                depends_on="eval:doc.delivery_status == \"Delivered\"",
                allow_on_submit=1,
                default="Attempt"
            ),
            dict(
                fieldname="mode_of_payment",
                fieldtype="Link",
                label="Mode of Payment",
                insert_after="delivery_status",
                in_preview=1,
                options="Mode of Payment",
                depends_on="eval:doc.delivery_status == \"Delivered\"",
            ),
            dict(
                fieldname="detail",
                fieldtype="Button",
                label="Details",
                insert_after="file_attachment",
                in_list_view=1,
            ),
            dict(
                fieldname="mobile",
                fieldtype="Data",
                label="Order Receiver Mobile",
                insert_after="mode_of_payment",
            ),
            dict(
                fieldname="file_attachment",
                fieldtype="Attach",
                label="File Attachment",
                insert_after="amount",
                allow_on_submit=1,
            ),
            ]        
    }
    create_custom_fields(custom_fields)
def delivery_stop_property_setter():
    make_property_setter("Delivery Stop", "contact", "in_preview", 1,"Check")
    make_property_setter("Delivery Stop", "details", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "uom", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "estimated_arrival", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "distance", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "customer_contact", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "email_sent_to", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "grand_total", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "delivery_note", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "visited", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "customer_address", "hidden", 1,"Check")
    make_property_setter("Delivery Stop", "lock", "hidden", 1,"Check")