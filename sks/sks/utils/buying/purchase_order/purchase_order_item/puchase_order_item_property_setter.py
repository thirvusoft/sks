import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def purchase_order_item_property_setter():
          make_property_setter("Purchase Order Item", "supplier_part_no", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "image", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "pricing_rules", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "material_request_item", "Hidden", 1, "Check") 
          make_property_setter("Purchase Order Item", "sales_order_item", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "supplier_quotation_item", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "item_group", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "brand", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "item_tax_rate", "Hidden", 1, "Check") 
          make_property_setter("Purchase Order Item", "production_plan_item", "Hidden", 1, "Check")
          make_property_setter("Purchase Order Item", "production_plan_sub_assembly_item", "Hidden", 1, "Check")