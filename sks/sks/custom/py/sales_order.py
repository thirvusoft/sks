import frappe
@frappe.whitelist(allow_guest=True)
def customer_transaction_history(customer): 
    from datetime import datetime   
    data = frappe.get_all("Sales Invoice",filters={'docstatus':1,'customer':customer},limit=10)
    item_list={}
    creation_date={}
    today = datetime.now()
    for i in data[::-1]:
        item_rate={}
        invoice_item=[]
        doc = frappe.get_doc("Sales Invoice",i['name'])
        items=doc.items
        date = today - doc.creation
        item_rate={k.rate:k.item_code for k in items}
        rates=list(item_rate.keys())
        rates.sort(reverse=True)
        if(len(rates)>8):rates=rates[:8:]
        for j in items:
            if(j.rate in rates):invoice_item.append(str(j.item_name + " (" + j.item_code + ")"))
        if(date.days == 0):creation_date[i['name']] = ['Today']
        else:creation_date[i['name']] = [str(date.days)+" days ago"]
        invoice_item=", ".join(invoice_item)
        invoice_item=[frappe.bold(i['name'])+":   &#12288"+invoice_item+"&#12288"]   
        item_list[i['name']] = invoice_item
    item_code_dict = frappe.db.get_list("Item",fields=['item_code'],filters={'disabled':0})
    item_code=[]
    for i in item_code_dict:
        item_code.append(i['item_code'])
    return item_list, creation_date,item_code


@frappe.whitelist()
def item_append(item_code=None,current_document=None):
	if(item_code!=None):
		item_code=eval(item_code)
		length_item_list=len(item_code)
		for i in range(0,length_item_list,1):
			doc = frappe.get_doc("Sales Order",current_document)
			doc.append("items",
				{"item_code" :item_code[i],"qty":1
			})
			doc.save()
		return 0


@frappe.whitelist()
def subwarehouse(sub_warehouse,company):
	sub_warehouse_list=[sub_warehouse]
	ware_house=[]
	while(True):
		sub_warehouse1=[]
		for i in sub_warehouse_list:
			data = frappe.get_all("Warehouse",fields=['name','is_group','parent_warehouse'],filters={"parent_warehouse":i,"company":company})
			for i in data:
				if(i.is_group == 0):
					ware_house.append(i.name)
				else:
					sub_warehouse1.append(i.name)
			data = frappe.get_all("Warehouse",fields=['name','is_group','parent_warehouse'],filters={'parent_warehouse':sub_warehouse,'company':'company'})
		sub_warehouse_list=sub_warehouse1
		if(len(sub_warehouse_list) == 0):
			break
	if(len(ware_house) == 0):
		ware_house.append(sub_warehouse)
	bin_data = frappe.get_all("Bin",fields=['item_code','actual_qty','warehouse'],filters={'actual_qty':('>',0),'warehouse':('in',ware_house)})
	item_warehouse={i['item_code']:i['warehouse'] for i in bin_data}
	items=list(item_warehouse.keys())
	return items
