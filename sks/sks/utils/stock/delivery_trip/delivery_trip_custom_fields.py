from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from sks.sks.utils.stock.delivery_trip.delivery_stop.delivery_stop_custom_fields import delivery_stop_customization
def delivery_trip_customization():
    delivery_trip_fields()
    delivery_trip_property_setter()
    delivery_stop_customization()
def delivery_trip_fields():
    custom_fields = {
        "Delivery Trip": [

            dict(
                fieldname="delivery_date",
                fieldtype="Date",
                insert_after="email_notification_sent",
                label="Delivery Date",
                options="Mode of Payment",
                default="Today"
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
        make_property_setter("Delivery Trip", "delivery_stops", "label", "Sales Invoice","Data")
        make_property_setter("Delivery Trip", "driver_address", "hidden", "1","Check")
        make_property_setter("Delivery Trip", "status", "hidden", "1","Check")