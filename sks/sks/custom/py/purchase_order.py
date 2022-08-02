import frappe
from frappe.model import document
# def last_purchase_price_validate(doc,event):
#     items_code=[]
#     items_rate=[]
#     items_price_changed=[]
#     for row in doc.items:
#         items_code.append(row.item_code)
#         items_rate.append(row.rate)
#     for i in range(0,len(items_code),1):
#         item_details=frappe.get_all("Item",fields=["name","last_purchase_rate"],filters={"name":items_code[i]})
#         item_last_rate=int(item_details[0]["last_purchase_rate"])
#         if(items_rate[i]!=item_last_rate):
#             items_price_changed.append(items_code[i])
#             price_changed_items = ",".join(items_price_changed)
#     doc.item_price_changed = price_changed_items

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
    
def warehouse_fetching(doc,event):
    item = doc.items
    items_with_no_warehouse=""
    for i in item:
        item_name =  frappe.get_doc("Item",i.item_code)
        if item_name.warehouse:
            for warehouse in item_name.warehouse:
                if warehouse.company:
                    if warehouse.company == doc.company:
                        w_house = warehouse.warehousebin
                        if w_house:i.warehouse = w_house
        else:
            items_with_no_warehouse+="•"+item_name.item_code+'<br>'
    if items_with_no_warehouse:frappe.throw(_("Please Select warehouse for <br>{0}".format(items_with_no_warehouse)))