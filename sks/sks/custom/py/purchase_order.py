from email import message
import frappe
@frappe.whitelist()
def last_purchase_price_validate(items_code,items_rate):
    items_code=eval(items_code)
    items_rate=eval(items_rate)
    items_price_changed=[]
    for i in range(0,len(items_code),1):
        item_details=frappe.get_all("Item",fields=["name","last_purchase_rate"],filters={"name":items_code[i]})
        item_last_rate=int(item_details[0]["last_purchase_rate"])
        if(items_rate[i]!=item_last_rate):
            items_price_changed.append(items_code[i])
    return ",".join(items_price_changed)

def validate_buying_rate_with_mrp(doc,event):
    value_changed_items=""
    for item in doc.items:
        if(item.rate and item.ts_mrp):
            buying_rate = item.rate
            mrp = item.ts_mrp
            if mrp<=buying_rate:
                value_changed_items+=f"• {item.item_code}<br>"
    if(value_changed_items):
        frappe.throw(title=frappe._("Items with higher buying rate than MRP"), msg=frappe._(value_changed_items))

