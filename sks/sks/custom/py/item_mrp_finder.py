import frappe
@frappe.whitelist()
def ts_mrp_finder(ts_item_code):
	ts_batch=frappe.get_all("Batch",fields=["name","posa_btach_price","item","expiry_date","creation","ts_mrp"])
	ts_matched_creation_date=[]
	ts_matched_batch_name=[]
	ts_item_mrp=0
	for j in range(0,(len(ts_batch)),1):
			if(ts_item_code==ts_batch[j]["item"]):
				ts_matched_batch_name.append(ts_batch[j]["name"])
	for l in range(0,len(ts_matched_batch_name),1):
		for n in range(0,(len(ts_batch)),1):
			if(ts_matched_batch_name[l]==ts_batch[n]["name"]):
				ts_matched_creation_date.append(ts_batch[n]["creation"])
	for c in range(0,(len(ts_batch)),1):
		if(ts_matched_creation_date!=[]):
			if(max(ts_matched_creation_date)==ts_batch[c]["creation"]):
				ts_item_mrp=ts_batch[c]["ts_mrp"]
	return(ts_item_mrp)