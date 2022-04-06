import frappe
@frappe.whitelist()
def item_check_with_purchase_order(item_code_checking=None,checking_purchase_order=None):
	matched_item=0
	item_code_from_purchase_order=frappe.get_doc("Purchase Order",checking_purchase_order)
	total_item=item_code_from_purchase_order.__dict__["items"]
	len_items=len(total_item)
	if(item_code_checking != None):
		for j in range(0,len_items,1):
			if(item_code_checking == total_item[j].__dict__["item_code"]):
				item_code=total_item[j].__dict__["item_code"]
				matched_item=matched_item+1
				break
	if(matched_item==1):
		matched_item=0
		return item_code
	else:
		return 0
	
@frappe.whitelist()
def adding_barcode(barcode,item_code):
	item_barcode=frappe.get_doc("Item",item_code)
	item_barcode.append('barcodes',{'barcode':barcode})
	item_barcode.save()

from frappe.utils import getdate
@frappe.whitelist()
def auto_batch_creation(expiry_date=None,item_rate=None,item_code=None,total_barcode_number_item=None,total_barcode_item_code=None,against_purchase_order_name=None,doctype_name=None,document_name=None):
    expiry_date=eval(expiry_date)
    item_rate=eval(item_rate)
    item_code=eval(item_code)
    total_barcode_item_code=eval(total_barcode_item_code)
    total_barcode_number_item=eval(total_barcode_number_item)
    matched_batch_name=[]
    matched_creation_date=[]
    item_changes_count=0
    item_changes_details=[]
    batch_expiry=frappe.get_all("Batch",fields=["name","item","expiry_date","creation"])
    for i in range(0,len(item_code),1):
        for j in range(0,(len(batch_expiry)),1):
                if(item_code[i]==batch_expiry[j]["item"]):
                    matched_batch_name.append(batch_expiry[j]["name"])
        for l in range(0,len(matched_batch_name),1):
            for n in range(0,(len(batch_expiry)),1):
                if(matched_batch_name[l]==batch_expiry[n]["name"]):
                    matched_creation_date.append(batch_expiry[n]["creation"])
        for c in range(0,(len(batch_expiry)),1):
            if(matched_creation_date!=[]):
                if(max(matched_creation_date)==batch_expiry[c]["creation"]):
                    correct_batch_name=batch_expiry[c]["name"]
                    formatted_expiry_date=getdate(expiry_date[i])
                    if(batch_expiry[c]["expiry_date"]!=formatted_expiry_date):
                        item_changes_count=item_changes_count+1
                        item_changes_details.append("Expiry date")
        for b in range(0,len(total_barcode_item_code),1):
            if(item_code[i]==total_barcode_item_code[b]):
                item_changes_count=item_changes_count+1
                item_changes_details.append("Barcode")
                changed_barcode=total_barcode_number_item[b]
        items_price_changed=frappe.get_doc("Purchase Order",against_purchase_order_name)
        items_price_changed_list=items_price_changed.__dict__["item_price_changed"].split(",")
        for p in range(0,len(items_price_changed_list),1):
            if(item_code[i]==items_price_changed_list[p]):
                item_changes_count=item_changes_count+1
                item_changes_details.append("Price")
        item_document=frappe.get_doc(doctype_name,document_name)
        if(item_changes_count==0):
            frappe.db.set_value("Item",item_code[i],"create_new_batch",0)
            for item in item_document.items:
                if(item_code[i]==item.__dict__["item_code"]):
                    frappe.set_value(item.doctype,item.name,"batch_no",correct_batch_name)
        else:
            for item in item_document.items:
                if(item_code[i]==item.__dict__["item_code"]):
                    # frappe.set_value(item.doctype,item.name,"barcode",changed_barcode)
                    pass
            frappe.db.set_value("Item",item_code[i],"create_new_batch",1)
        item_changes_count=0
        item_changes_details=[]
    return 0
        
        

