from sks.sks.utils.buying.purchase_order.purchase_order_custom_fields import purchase_order_customization
from sks.sks.utils.buying.purchase_receipt.purchase_receipt_custom import purchase_receipt_customization
from sks.sks.utils.buying.purchase_invoice.purchase_invoice_custom_fields import purchase_invoice_customization
def after_install():
          purchase_order_customization()
          purchase_receipt_customization()
          purchase_invoice_customization()