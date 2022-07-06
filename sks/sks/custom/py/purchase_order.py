from audioop import avgpp
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

@frappe.whitelist()
def last_purchased_and_sold_qty(ts_item_code):
    last_purchase_qty = (frappe.db.sql("""select purchase_qty 
                                        from `tabBatch`
                                        where item = '{0}'
                                        order by MAX(manufacturing_date)
                                        limit 1; 
                                        """.format(ts_item_code),as_list=1))[0][0]
    Available_qty = (frappe.db.sql("""select batch_qty 
                                        from `tabBatch`
                                        where item = '{0}'
                                        order by MAX(manufacturing_date)
                                        limit 1; 
                                        """.format(ts_item_code),as_list=1))[0][0]
    sold_qty=0
    if(last_purchase_qty and Available_qty):
        sold_qty = last_purchase_qty - Available_qty
    return last_purchase_qty,sold_qty
    
