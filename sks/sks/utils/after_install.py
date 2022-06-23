from sks.sks.utils.buying.purchase_order.purchase_order_custom_fields import purchase_order_customization
from sks.sks.utils.buying.purchase_receipt.purchase_receipt_custom import purchase_receipt_customization
from sks.sks.utils.buying.purchase_invoice.purchase_invoice_custom_fields import purchase_invoice_customization          
from sks.sks.utils.selling.delivery_note.delivery_note_custom_fields import delivery_note_customization
from sks.sks.utils.selling.sales_order.sales_order_custom_fields import sales_order_customization
from sks.sks.utils.selling.sales_invoice.sales_invoice_custom_fields import sales_invoice_customization
from sks.sks.utils.stock.item.item_custom_fields import item_customization
from sks.sks.utils.crm.customer.customer_custom_fields import customer_customization
from sks.sks.utils.stock.item.item_barcode_custom_fields import item_barcode_customization
from sks.sks.utils.stock.item.item_tax_custom_fields import item_tax_customization
from sks.sks.utils.stock.material_request.material_request_custom_fields import material_request_customization
from sks.sks.utils.stock.batch.batch_custom_fields import batch_customization
from sks.sks.utils.stock.delivery_trip.delivery_trip_custom_fields import delivery_trip_customization
from sks.sks.utils.crm.contact.contact_custom_fields import contact_customization
from sks.sks.utils.hr.driver.driver_custom_fields import driver_customization
from sks.sks.utils.crm.address.address_custom_fields import address_customization
from sks.sks.utils.selling.delivery_note.packed_item.packed_item_custom_fields import packed_item_customization
def after_install():
    purchase_order_customization()
    delivery_note_customization()
    sales_order_customization()
    sales_invoice_customization()
    item_customization()
    purchase_invoice_customization()
    purchase_receipt_customization()
    customer_customization()
    item_tax_customization()
    item_barcode_customization()
    material_request_customization()
    batch_customization()
    delivery_trip_customization()
    contact_customization()
    driver_customization()
    address_customization()
    packed_item_customization()