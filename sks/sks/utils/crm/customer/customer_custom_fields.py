from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def customer_customization():
    customer_custom_fields()
    customer_property_setter()
def customer_custom_fields():
    custom_fields = {
        "Customer":[
            dict(
                fieldname="is_pickup_customer",
                fieldtype="Check",
                label="Is Pickup Customer",
                insert_after="is_internal_customer",
                allow_in_quick_entry=1,
                ),
            dict(
                fieldname="is_door_delivery_customer",
                fieldtype="Check",
                label="Is Door Delivery Customer",
                insert_after="is_pickup_customer",
                allow_in_quick_entry=1,
                ),
            dict(
                fieldname="is_credit_customer",
                fieldtype="Check",
                label="Is Credit Customer",
                insert_after="is_door_delivery_customer",
                allow_in_quick_entry=1
                ),
            dict(
                fieldname="feedback_required",
                fieldtype="Check",
                label="Feedback Required",
                insert_after="is_credit_customer",
                allow_in_quick_entry=1,
                ),
            dict(
                fieldname="name_in_tamil_",
                fieldtype="Data",
                label="\u0bb5\u0bbe\u0b9f\u0bbf\u0b95\u0bcd\u0b95\u0bc8\u0baf\u0bbe\u0bb3\u0bb0\u0bbf\u0ba9\u0bcd \u0baa\u0bc6\u0baf\u0bb0\u0bcd",
                insert_after="customer_name",
                )
    ]
    }
    create_custom_fields(custom_fields)
def customer_property_setter():                
    make_property_setter("Customer","credit_limit_section","depends_on","eval:doc.is_credit_customer == 1","Data")
    make_property_setter("Customer","sales_team_section","hidden",1,"Check")
    make_property_setter("Customer","sales_team_section_break","hidden",1,"Check")
    make_property_setter("Customer","more_info","hidden",1,"Check")
    make_property_setter("Customer","naming_series","reqd",0,"Check")
    make_property_setter("Customer","naming_series","hidden",1,"Check")
    make_property_setter("Customer", "customer_type", "default", "Individual", "Data")
    make_property_setter("Customer", "customer_type", "reqd", "0", "Check")
    make_property_setter("Customer", "is_credit_customer", "allow_in_quick_entry", "0", "Check")
    make_property_setter("Customer", "feedback_required", "allow_in_quick_entry", "0", "Check")
    make_property_setter("Customer", "posa_referral_code", "allow_in_quick_entry", "0", "Check")
    make_property_setter("Customer", "posa_referral_company", "allow_in_quick_entry", "0", "Check")
    make_property_setter("Customer", "posa_referral_company", "hidden", "1", "Check")
    make_property_setter("Customer", "mobile_no", "unique", "1", "Check")
    make_property_setter("Customer", "customer_group", "default", "Individual", "Link")
    make_property_setter("Customer", "tax_category", "default", "In-State", "Link")
    make_property_setter("Customer", "customer_type", "default", "Individual", "Select")
    make_property_setter("Customer", "gst_category", "default", "Unregistered", "Select")


