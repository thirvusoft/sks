from sks.sks.utils.buying.purchase_order.purchase_order_custom_fields import purchase_order_customization
from sks.sks.utils.selling.delivery_note.delivery_note_custom_fields import  delivery_note_customization
def after_install():
    purchase_order_customization()
    delivery_note_customization()