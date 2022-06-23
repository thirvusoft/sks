from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def delivery_trip_customization():
    delivery_trip_fields()
    delivery_trip_property_setter()
def delivery_trip_fields():
    custom_fields = {
        "Delivery Trip": [
            dict(
                fieldname="reason",
                fieldtype="Data",
                label="Reason",
                insert_after="mode_of_payment"
            ),
            dict(
                fieldname="time_of_delivery",
                fieldtype="Time",
                label="Time of Delivery",
                insert_after="reason"
            ),
            dict(
                fieldname="sales_invoice",
                fieldtype="Link",
                label="Reason",
                options="Sales Invoice",
                insert_after="delivery_stop_helper"
            ),
            dict(
                fieldname="amount",
                fieldtype="Data",
                label="Amount",
                insert_after="time_of_delivery"
            ),
            dict(
                fieldname="column_break_19",
                fieldtype="Column Break",
                insert_after="update_invoice"
            ),
            dict(
                fieldname="delivery_status",
                fieldtype="Select",
                insert_after="sales_invoice",
                label="Delivery Status",
                options="Attempt\nDelivered\nNot Delivered\nReady To Dispatch\nReattempt\nReturned",
            ),
            dict(
                fieldname="delivery_stop_helper",
                fieldtype="Section Break",
                insert_after="employee",
                label="Delivery Stop Helper",
            ),
            dict(
                fieldname="mode_of_payment",
                fieldtype="Link",
                insert_after="column_break_19",
                label="Mode of Payment",
                options="Mode of Payment"
            ),
            dict(
                fieldname="update_invoice",
                fieldtype="Button",
                insert_after="delivery_status",
                label="Update Invoice",
                options="Mode of Payment"
            ),
            dict(
                fieldname="delivery_date",
                fieldtype="Date",
                insert_after="email_notification_sent",
                label="Delivery Date",
                options="Mode of Payment",
                default="Today"

            ),
            dict(
                fieldname="delivered_driver",
                fieldtype="Link",
                insert_after="section_break_3",
                label="Delivered Driver",
                options="TS Driver Delivery Trip",
                
            ),
            dict(
                fieldname="user_id",
                fieldtype="Link",
                fetch_from="driver.user_id",
                insert_after="driver_name",
                label="User ID",
                options="User",
                read_only=1,
                
            ),
            ],      
    }
    create_custom_fields(custom_fields)
def delivery_trip_property_setter():                
        make_property_setter("Delivery Trip", "delivery_stops", "allow_on_submit", 1,"Check")
        make_property_setter("Delivery Trip", "email_notification_sent", "hidden", "1","Check")