import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_order_item_custom_fields():
          custom_fields = {
          "Purchase Order Item": [
                    dict(
                              allow_on_submit= 1,
                              fetch_from= "item_code.gst_hsn_code",
                              fetch_if_empty= 1,
                              fieldname= "gst_hsn_code",
                              fieldtype= "Data",
                              insert_after= "description",
                              label= "HSN/SAC",
                              print_hide= 1,
                              translatable= 1,
                              unique= 0,
                    ),
                    dict(
                              fetch_from= "item_code.is_nil_exempt",
                              fieldname= "is_nil_exempt",
                              fieldtype= "Check",
                              insert_after= "gst_hsn_code",
                              label= "Is Nil Rated or Exempted",
                              print_hide= 1,
                              translatable= 1,
                    ),
                    dict(
                              fetch_from= "item_code.is_non_gst",
                              fieldname= "is_non_gst",
                              fieldtype= "Check",
                              insert_after= "is_nil_exempt",
                              label= "Is Non GST",
                              print_hide= 1,
                              translatable= 1,
                    ),
                    dict(
                              fieldname= "ts_mrp",
                              fieldtype= "Currency",
                              in_list_view= 1,
                              insert_after= "sec_break2",
                              label= "MRP",
                    ),
                      dict(fieldname='ts_warehouse', label='TS Warehouse',
                fieldtype='Data', hidden=0,insert_after='warehouse')
          ],
          }
          create_custom_fields(custom_fields)
def purchase_order_item_property_setter():
    make_property_setter("Purchase Order Item", "supplier_part_no", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "image", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "pricing_rules", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "material_request_item", "hidden", 1, "Check") 
    make_property_setter("Purchase Order Item", "sales_order_item", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "supplier_quotation_item", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "item_group", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "brand", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "item_tax_rate", "hidden", 1, "Check") 
    make_property_setter("Purchase Order Item", "production_plan_item", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "production_plan_sub_assembly_item", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "is_nil_exempt", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "is_non_gst", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "section_break_72", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "accounting_details", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "against_blanket_order", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "sales_order", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "sales_order_packed_item", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "manufacture_details", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "item_weight_details", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "section_break_5", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "project", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "amount", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "base_net_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "base_net_amount", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "stock_uom_rate", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "sec_break1", "hidden", 1, "Check")
    make_property_setter("Purchase Order Item", "expected_delivery_date", "hidden", 1, "Check")