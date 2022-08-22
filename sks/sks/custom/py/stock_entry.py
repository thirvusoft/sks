import frappe
from frappe import _
def stock_entry(doc,action):
	item_wise_batch_details=[]
	if doc.stock_entry_type == "Repack":
		for item_source_warehouse in doc.items:
			if item_source_warehouse.s_warehouse:
				item_wise_batch_details.append(frappe.get_value("Batch",item_source_warehouse.batch_no,"ts_valuation_rate"))
				item_source_warehouse.basic_rate = item_source_warehouse.valuation_rates
		for item_target_warehouse in doc.items:
			if item_target_warehouse.t_warehouse:
				item_target_warehouse.valuation_rates = sum(item_wise_batch_details)
		markup_and_markdown_calculator(doc)

def markup_and_markdown_calculator(document):
	if document.stock_entry_type == "Repack":
		ts_matched_item=[]
		ts_matched_selling_rate=[]
		for item in document.items:
			if item.t_warehouse:
				item_code = item.item_code
				v_rate = item.valuation_rates
				ts_item_detais=frappe.get_doc("Item",item_code)
				if ts_item_detais:
					item_mrp = ts_item_detais.mrp
					if(ts_item_detais.__dict__["select_selling_price_type"]=="Markdown"):
						ts_markdown=(item_mrp/100)*ts_item_detais.__dict__["ts_markdown_price"]
						ts_markdown=item_mrp-ts_markdown
						if(ts_markdown<item_mrp and ts_markdown>v_rate):
							ts_matched_item.append(item_code)
							ts_matched_selling_rate.append(ts_markdown)
							item.selling_rates = ts_matched_selling_rate[0]
						else:
							frappe.throw(_("In Markdown, The selling rate is lesser then the valuation rate for the below item please contact higher authority people <br>•{0}").format(ts_item_detais.name))
					
					
					if(ts_item_detais.__dict__["select_selling_price_type"]=="Markup"):
						ts_markup=(item_mrp/100)*ts_item_detais.__dict__["ts_markup_price"]
						ts_markup=v_rate+ts_markup
						if(ts_markup<item_mrp and ts_markup>v_rate):
							ts_matched_item.append(item_code)
							ts_matched_selling_rate.append(ts_markup)
							item.selling_rates = ts_matched_selling_rate[0]    
						else:
							frappe.throw(_("In Markup, The selling rate is greater then the MRP for the below item please contact higher authority people <br>•{0}").format(ts_item_detais.name))
	
@frappe.whitelist()
def auto_batch_creations(doc,event):
	access=frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation")
	if access==1:
		item_rate=[]
		item_code=[]
		item_mrp=[]
		# expiry_date=[]
		for item in doc.items:
			single_batch_item = frappe.db.get_value("Item",{"item_code":item.item_code},"is_single_batch")
			if single_batch_item == 0:
				if item.t_warehouse:
					item_rate.append(item.valuation_rates)
					item_code.append(item.item_code)
					item_mrp.append(item.mrp_rates)
					# expiry_date.append(item.expire_dates)
			else:
				if item.t_warehouse:
					single_batch = frappe.db.get_value("Batch",{"item":item.item_code},"name")
					if single_batch:
						item.batch_no=single_batch
					else:
						frappe.db.set_value("Item",item.item_code,"create_new_batch",1)
		item_changes_count=0
		item_changes_details=[]
		for i in range(0,len(item_code),1):
			try:
				if(frappe.db.get_value("Item",{"name":item_code[i]},["is_expiry_item"])):
					batch_doc = frappe.get_last_doc("Batch", filters = [["item","=", item_code[i]],['expiry_date','>=',nowdate()]],order_by="modified desc")
				else:
					batch_doc = frappe.get_last_doc("Batch", filters = [["item","=", item_code[i]]],order_by="modified desc")

				if(batch_doc.ts_mrp!=item_mrp[i]):
					item_changes_count=item_changes_count+1
					item_changes_details.append("MRP")
				if(batch_doc.ts_valuation_rate!=item_rate[i]):
					item_changes_count=item_changes_count+1
					item_changes_details.append("Valuation Rate")
				# if batch_doc.expiry_date:
				# 	ts_date=getdate(expiry_date[i])
				# 	if(batch_doc.expiry_date!=ts_date):
				# 		item_changes_count=item_changes_count+1
				# 		item_changes_details.append("Valuation Rate")
			except:
				batch_doc = 0

			if(item_changes_count==0) and batch_doc:
				frappe.db.set_value("Item",item_code[i],"create_new_batch",0)
				for item in doc.items:
					if(item_code[i]==item.__dict__["item_code"]):
						if(batch_doc.name!=0):
							item.batch_no=batch_doc.name
			else:
				frappe.db.set_value("Item",item_code[i],"create_new_batch",1)
				for item in doc.items:
					if(item_code[i]==item.__dict__["item_code"]):
						pass
						# item.batch_no=""
			item_changes_count=0
			item_changes_details=[]

@frappe.whitelist()
def material_transfer(doc,event):
	if (doc.stock_entry_type == "Material Transfer" or doc.stock_entry_type == "Repack"):
		not_verified_items=""
		for item in doc.items:
			item.valuation_rate=item.valuation_rates
			if doc.outgoing_stock_entry:
				if item.ts_material_transfer_verification == 0:
					not_verified_items += "•"+item.item_code+'<br>'

		if not_verified_items:
			frappe.throw(_("Below Items Are Not Verified, Please Check It... <br>{0}").format(not_verified_items))

def mandatory_validation(doc,event):
	# Expiry Date and Selling Price Validation
	ts_item_expiry_date=""
	ts_mrp_differ_selling_rate=""
	ts_valuation_differ_selling_rate=""
	if doc.stock_entry_type=="Material Receipt":
		for item in doc.items:
			if item.t_warehouse:
				ts_has_expiry=frappe.db.get_value("Item",{"name":item.item_code},["is_expiry_item"])
				if ts_has_expiry==1:
					if not item.expire_dates:
						ts_item_expiry_date += "•"+item.item_code+'<br>'

				if item.selling_rates > item.mrp_rates:
					ts_mrp_differ_selling_rate += "•"+item.item_code+'<br>'
				if item.selling_rates <= float(item.valuation_rates):
					ts_valuation_differ_selling_rate += "•"+item.item_code+'<br>'
				else: item.valuation_rate=item.valuation_rates
		if ts_item_expiry_date:
			frappe.throw(_("Please Select the Expiry Date For The Below Items... <br>{0}").format(ts_item_expiry_date))
		
		if ts_mrp_differ_selling_rate:
			frappe.throw(_("Selling Price Is Greater Than The MRP, Please Check It... <br>{0}").format(ts_mrp_differ_selling_rate))
		
		if ts_valuation_differ_selling_rate:
			frappe.throw(_("Selling Price Is Lesser Than The Valuation Rate, Please Check It... <br>{0}").format(ts_valuation_differ_selling_rate))

@frappe.whitelist()
def valuation_rate_fetching(batch_no):
	valuation_rate=frappe.db.get_value("Batch",{"name":batch_no},["ts_valuation_rate"])
	return valuation_rate