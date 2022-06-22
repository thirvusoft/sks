import frappe
from sks.sks.utils.buying.purchase_order.purchase_order_item.puchase_order_item_property_setter import purchase_order_item_property_setter
from sks.sks.utils.buying.purchase_order.purchase_order_item.purchase_order_item_custom_fields import purchase_order_item_custom_fields
def after_install():
          purchase_order_item_property_setter()
          purchase_order_item_custom_fields()
          purchase_order_custom_fields()
def purchase_order_custom_fields():
          pass