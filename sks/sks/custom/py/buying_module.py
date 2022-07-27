import frappe
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
                                        Order by modified DESC
                                        limit 1
                                        """.format(ts_item_code),as_list=1))
    if last_purchase_qty:
        last_purchase_qty = last_purchase_qty[0][0]
        
         
    Available_qty = (frappe.db.sql("""select batch_qty 
                                        from `tabBatch`
                                        where item = '{0}'
                                        order by modified DESC
                                        limit 1
                                        """.format(ts_item_code),as_list=1))
    if Available_qty:
        Available_qty = Available_qty[0][0]
    
    sold_qty=0
    if(last_purchase_qty and Available_qty):
        sold_qty = last_purchase_qty - Available_qty       
    return last_purchase_qty,sold_qty

@frappe.whitelist()    
def buying_rate_finder(ts_item_code):
    buying_margin_percentage = frappe.db.get_value("Item",{"item_code":ts_item_code},"buying_margin_percentage")
    item_mrp = frappe.db.get_value("Item",{"item_code":ts_item_code},"mrp")
    if(buying_margin_percentage > 0 and item_mrp > 0):
        buying_percentage_amount = (item_mrp/100)*buying_margin_percentage
        buying_rate = item_mrp-buying_percentage_amount
        return buying_rate
    
@frappe.whitelist()
def not_processed_po(ts_supplier):
    supplier_doc = frappe.get_list("Purchase Order",{"supplier":ts_supplier,"status":"To Receive and Bill"},pluck="name")
    ts_not_processed_po=[]
    for s_doc in supplier_doc:
        row = frappe._dict()
        row.update({'purchase_order':s_doc})
        ts_not_processed_po.append(row)
    return ts_not_processed_po

@frappe.whitelist()   
def fetching_items_from_not_processed_po(reqd_po):
    lists=[]
    items_list=[]
    reqd_po=eval(reqd_po)
    for po_doc in reqd_po:
        print(po_doc)
        items = frappe.db.sql(''' select item_code,qty
                                from `tabPurchase Order Item` as po
                                where parent='{0}';
                              '''.format(po_doc),as_dict=1)
        print(items)
        if items_list:
            item_code = [i['item_code'] for i in items_list]
            for i in items:
                if(i['item_code'] in item_code):
                    for j in items_list:
                        if(j['item_code'] == i['item_code']):j['qty'] += i['qty']
                else:
                    items_list.append(i)
        else:
            items_list=items
        frappe.msgprint(f"Cancelling Purchase Order : {po_doc}")
        cancel_doc=frappe.get_doc("Purchase Order",po_doc)
        cancel_doc.docstatus=2
        cancel_doc.save()
        frappe.db.commit()
    return items_list
