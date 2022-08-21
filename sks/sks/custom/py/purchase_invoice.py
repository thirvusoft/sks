import json
import frappe
from frappe import _
from frappe.utils import flt,getdate,nowdate
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

def automatic_batch_creation(doc,event):
	auto_batch=frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation")
	if auto_batch==1:
		# expiry_date=[]
		item_rate=[]
		item_mrp=[]
		item_code=[]
		item_changes_count=0
		item_changes_details=[]
		changed_barcode=0
		total_barcode_item_code=[]
		total_barcode_number_item=[]
		if doc.scanned_items:
			total_barcode_item_code = eval(doc.scanned_items)
		if doc.scanned_barcodes:
			total_barcode_number_item = eval(doc.scanned_barcodes)
		for row in doc.items:
			single_batch_item = frappe.db.get_value("Item",{"item_code":row.item_code},"is_single_batch")
			if single_batch_item == 0:
				item_code.append(row.item_code)
				# expiry_date.append(row.expiry_date)
				item_rate.append(row.ts_valuation_rate)
				item_mrp.append(row.ts_mrp)
			else:
				single_batch = frappe.db.get_value("Batch",{"item":row.item_code},"name")
				if single_batch:
					row.batch_no=single_batch
				else:
					frappe.db.set_value("Item",row.item_code,"create_new_batch",1)

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
				for b in range(0,len(total_barcode_item_code),1):
					if(item_code[i]==total_barcode_item_code[b]):
						item_changes_count=item_changes_count+1
						item_changes_details.append("Barcode")
						changed_barcode=total_barcode_number_item[b]
			except:
				batch_doc = 0

			if(item_changes_count==0) and batch_doc:
				frappe.db.set_value("Item",item_code[i],"create_new_batch",0)
				for item in doc.items:
					if(item_code[i]==item.__dict__["item_code"]):
						if(batch_doc.name!=0):
							item.batch_no=batch_doc.name
			else:
				if(total_barcode_number_item):
					for item in doc.items:
						if(item_code[i]==item.__dict__["item_code"]):
							if(changed_barcode!=0):
								item.barcode=changed_barcode
								item.batch_no=""
				frappe.db.set_value("Item",item_code[i],"create_new_batch",1)
			item_changes_count=0
			item_changes_details=[]

def markup_and_markdown_calculator(document,event):
	document.update({
					'thirvu_items_to_verify':{}
				})
	ts_items=document.items
	if ts_items:
		ts_val_rate=0
		ts_landed_cost_voucher_table=document.ts_landed_cost_voucher_table
		if ts_landed_cost_voucher_table:
			if document.type == 'Exclusive':
				ts_val_rate=1
				ts_valuation_details=calculating_landed_cost_voucher_amount(document)
				ts_val_item=[]
				ts_val_rate=[]
				ts_val_tot_item=ts_valuation_details[0]
				ts_val_tot_rate=ts_valuation_details[1]
				for v in range(0,len(ts_val_tot_item),1):
					ts_val_item.append(ts_val_tot_item[v])
					ts_val_rate.append(ts_val_tot_rate[v])
				for item in document.get('items'):
					for vi in range(0,len(ts_val_item),1):
						if ts_val_item[vi]==item.item_code:
							ts_rate=ts_val_rate[vi]
							ts_valuation_rate=ts_rate/item.qty

							# core function start
							qty_in_stock_uom = flt(item.qty * item.conversion_factor)
							item.ts_valuation_rate = (
								item.base_net_amount
								+ item.item_tax_amount
								+ item.rm_supp_cost
								+ flt(item.landed_cost_voucher_amount)
							) / qty_in_stock_uom + ts_valuation_rate
							item.valuation_rate = item.ts_valuation_rate
							# core function end
			else:
				for item in document.get('items'):
					item.ts_valuation_rate = item.valuation_rate
		else:
			for item in document.get('items'):

				# core function start
				qty_in_stock_uom = flt(item.qty * item.conversion_factor)
				item.ts_valuation_rate = (
					item.base_net_amount
					+ item.item_tax_amount
					+ item.rm_supp_cost
					+ flt(item.landed_cost_voucher_amount)
				) / qty_in_stock_uom
				item.valuation_rate = item.ts_valuation_rate

				# core function end
			else:
				item.ts_valuation_rate = item.valuation_rate
						

		ts_item_code=[]
		ts_item_name=[]
		ts_mrp=[]
		ts_selling_rate=[]
		ts_valuation_rate=[]
		for item in document.get('items'):
			ts_item_code.append(item.item_code)
			ts_item_name.append(item.item_name)
			ts_mrp.append(item.ts_mrp)
			ts_selling_rate.append(item.ts_selling_rate)
			ts_valuation_rate.append(item.ts_valuation_rate)
		 
		ts_unmatched_item=[]
		ts_unmatched_selling_rate=[]
		ts_matched_item=[]
		ts_matched_selling_rate=[]
		ts_markdown_items_to_verify = []
		ts_markup_items_to_verify = []
		ts_markup_items = ""
		ts_markdown_items = ""
		for i in range(0,len(ts_item_code),1):
			ts_item_detais=frappe.get_doc("Item",ts_item_code[i])
			if ts_item_detais:
				ts_item_detais.mrp=ts_mrp[i]
				ts_item_detais.save()
				if(ts_item_detais.__dict__["select_selling_price_type"]=="Markdown"):
					ts_markdown=(ts_mrp[i]/100)*ts_item_detais.__dict__["ts_markdown_price"]
					ts_markdown=ts_mrp[i]-ts_markdown
					if(ts_markdown<ts_mrp[i] and ts_markdown>ts_valuation_rate[i]):
						ts_matched_item.append(ts_item_code[i])
						ts_matched_selling_rate.append(ts_markdown)
					else:
						ts_unmatched_item.append(ts_item_code[i])
						ts_unmatched_selling_rate.append(ts_markdown)
						item_row = frappe._dict({})                                              
						item_row.update({'items':ts_item_code[i],'selling_rate':ts_markdown,'difference':round(abs(ts_valuation_rate[i]-ts_markdown),2)})
						ts_markdown_items_to_verify.append(item_row)
						ts_markdown_items += f"{ts_item_name[i]}:{round(abs(ts_mrp[i]-ts_markdown),2)}\n"
							
						
				elif(ts_item_detais.__dict__["select_selling_price_type"]=="Markup"):
					ts_markup=(ts_mrp[i]/100)*ts_item_detais.__dict__["ts_markup_price"]
					ts_markup=ts_valuation_rate[i]+ts_markup
					if(ts_markup<ts_mrp[i] and ts_markup>ts_valuation_rate[i]):
						ts_matched_item.append(ts_item_code[i])
						ts_matched_selling_rate.append(ts_markup)
					else:
						ts_unmatched_item.append(ts_item_code[i])
						ts_unmatched_selling_rate.append(ts_markup)
						item_row = frappe._dict({})                                              
						item_row.update({'items':ts_item_code[i],'selling_rate':ts_markup,'difference':round(abs(ts_mrp[i]-ts_markup),2)})
						ts_markup_items_to_verify.append(item_row)
						ts_markup_items += f"{ts_item_name[i]}:{round(abs(ts_valuation_rate[i]-ts_markup),2)}\n"
		document.ts_markdown_items = ts_markdown_items
		document.ts_markup_items = ts_markup_items
		for item in document.get('items'):
			for m in range (0,len(ts_matched_item),1):
				if item.item_code==ts_matched_item[m]:
					item.ts_selling_rate=ts_matched_selling_rate[m]
					item.ts_selling_rate_automatic_calculation=1
			for m in range (0,len(ts_unmatched_item),1):
				if item.item_code==ts_unmatched_item[m]:
					item.ts_selling_rate=ts_unmatched_selling_rate[m]
					item.ts_selling_rate_automatic_calculation=1

		# Markup & Markdown
		markup_down_verification = frappe.db.get_single_value('Thirvu Retail Settings',"verification_of_markup_and_down")
		if markup_down_verification == 1:
			costing_details = []
			if(ts_markup_items_to_verify):
				for i in range(0,len(ts_markup_items_to_verify),1):
					ts_markup_items_to_verify_ = [{
							'items':ts_markup_items_to_verify[i]['items'],
							'markup__markdown':"Markup",
							'selling_rate':ts_markup_items_to_verify[i]['selling_rate'],
							'difference':ts_markup_items_to_verify[i]['difference'],
							}]
					document.update({
							'thirvu_items_to_verify':costing_details+ts_markup_items_to_verify_
						})
			costing_details= document.get('thirvu_items_to_verify') or []
			if(ts_markdown_items_to_verify):
				for i in range(0,len(ts_markdown_items_to_verify)):
					ts_markdown_items_to_verify_ = [{
							'items':ts_markdown_items_to_verify[i]['items'],
							'markup__markdown':"MarkDown",
							'selling_rate':ts_markdown_items_to_verify[i]['selling_rate'],
							'difference':ts_markdown_items_to_verify[i]['difference'],
							}]
					document.update({
							'thirvu_items_to_verify':costing_details+ts_markdown_items_to_verify_
						})
			if(len(document.thirvu_items_to_verify)>0):document.ts_markup_and_markdown_variations=1
			else:
				document.ts_markup_and_markdown_variations=0

def calculating_landed_cost_voucher_amount(self):
	total_item_cost = 0.0
	total_charges = 0.0
	item_count = 0
	ts_item_code=[]
	ts_separate_amount=[]
	based_on_field = frappe.scrub(self.ts_distribute_charges_based_on)
	for item in self.get('items'):
			total_item_cost += item.get(based_on_field)
	for item in self.get('items'):
			ts_total_value = flt(flt(item.get(based_on_field)) * (flt(self.ts_total_amount) / flt(total_item_cost)),
				)
			total_charges += ts_total_value
			item_count += 1
			ts_item_code.append(item.item_code)
			ts_separate_amount.append(ts_total_value)
	return ts_item_code,ts_separate_amount

@frappe.whitelist()
def validate(doc,event):
	doc.update_stock = 1
	alter_verification = frappe.db.get_single_value('Thirvu Retail Settings',"verification_of_altered_quantity")
	if alter_verification:
		#Altered Qty
		list = []
		doc.set('thirvu_altered_quantity',[])
		for item in doc.items:
			if item.purchase_order:
				po_doc = frappe.get_doc('Purchase Order',item.purchase_order)
				for po_items in po_doc.items:
					item_row=frappe._dict()
					if po_items.item_code == item.item_code:
						if int(po_items.qty) < int(item.qty):
							item_row.update({'ts_item':item.item_code,"ts_qty":int(po_items.qty),'ts_aqty':item.qty,'difference':int(item.qty) - int(po_items.qty)})
							list.append(item_row)
		doc.update({'thirvu_altered_quantity':list})
	
	reject_verification = frappe.db.get_single_value('Thirvu Retail Settings',"verification_of_rejected_quantity")
	if reject_verification:
		#Rejected Qty
		total_rejected_qty=0
		for item in doc.items:
			if item.purchase_order:
				po_doc = frappe.get_doc('Purchase Order',item.purchase_order)
				for po_items in po_doc.items:
					if po_items.item_code == item.item_code:
						if item.rejected_qty:
							total_rejected_qty+=item.rejected_qty
		doc.total_rejected_qty=total_rejected_qty
	
	price_change_verification = frappe.db.get_single_value('Thirvu Retail Settings',"verification_of_rate_change")
	if price_change_verification:
		#Price Changed Items
		price_changed = []
		doc.set('thirvu_price_changed_items',[])
		for item in doc.items:
			if item.purchase_order:
				po_docs = frappe.get_doc('Purchase Order',item.purchase_order)
				for po_item in po_docs.items:
					item_row=frappe._dict()
					if po_item.item_code == item.item_code:
						if po_item.rate > item.rate:
							item_row.update({'ts_item':item.item_code,"ts_original_price":po_item.rate,'ts_altered_price':item.rate,'difference':item.rate - po_item.rate})
							price_changed.append(item_row)
						elif po_item.rate < item.rate:
							item_row.update({'ts_item':item.item_code,"ts_original_price":po_item.rate,'ts_altered_price':item.rate,'difference':item.rate - po_item.rate})
							price_changed.append(item_row)
		doc.update({'thirvu_price_changed_items':price_changed})
		if(len(doc.thirvu_price_changed_items)>0):doc.ts_item_price_changed=1
		else:
			doc.ts_item_price_changed=0
	
def purchased_qty_validation(doc,event):
	thirvu_settings = frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation")
	if(thirvu_settings == 1):
		for items in doc.items:
			batch=items.batch_no
			purchased_qty=frappe.db.sql("""select sum(qty)
								from `tabPurchase Invoice Item`
								where batch_no ='{0}' and docstatus = 1""".format(batch),as_list=1)
			if purchased_qty[0][0]!=None:
				frappe.db.set_value("Batch",batch,"purchase_qty",purchased_qty[0][0])

def supplier_free_item(doc,event):
	verification = frappe.db.get_single_value('Thirvu Retail Settings',"verification_of_free_item")
	if verification:
		supplierfreeitem=[]
		doc.set('to_verify_free_item_from_supplier',[]) 
		for item in doc.items:
			if(item.is_free_item_from_supplier==1):
				row=frappe._dict()
				row.update({'item':item.item_code,'quantity':item.qty,'selling_rate':item.ts_selling_rate})
				supplierfreeitem.append(row)
		doc.update({'to_verify_free_item_from_supplier':supplierfreeitem})

@frappe.whitelist()
def mandatory_validation(doc,event):
	# Expiry Date and Selling Price Validation
	ts_item_expiry_date=""
	ts_mrp_differ_selling_rate=""
	ts_valuation_differ_selling_rate=""
	for item in doc.items:
		ts_has_expiry=frappe.db.get_value("Item",{"name":item.item_code},["is_expiry_item"])
		if ts_has_expiry==1:
			if not item.expiry_date:
				ts_item_expiry_date += "•"+item.item_code+'<br>'

		if item.ts_selling_rate_automatic_calculation !=1:
			if item.ts_selling_rate > item.ts_mrp:
				ts_mrp_differ_selling_rate += "•"+item.item_code+'<br>'

			if item.ts_selling_rate <= item.ts_valuation_rate:
				ts_valuation_differ_selling_rate += "•"+item.item_code+'<br>'
	
	if ts_item_expiry_date:
		frappe.throw(_("Please Select the Expiry Date For The Below Items... <br>{0}").format(ts_item_expiry_date))
	
	if ts_mrp_differ_selling_rate:
		frappe.throw(_("Selling Price Is Greater Than The MRP, Please Check It... <br>{0}").format(ts_mrp_differ_selling_rate))
	
	if ts_valuation_differ_selling_rate:
		frappe.throw(_("Selling Price Is Lesser Than The Valuation Rate, Please Check It... <br>{0}").format(ts_valuation_differ_selling_rate))
	
	# Warehouse Validation
	ts_value=frappe.db.get_single_value("Thirvu Retail Settings","item_warehouse_fetching")
	if ts_value==1:   
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

	# Barcode Veification validation
	ts_value=frappe.db.get_single_value("Thirvu Retail Settings","item_verifed_in_purchase_invoice")
	if ts_value==1:
		ts_item_barcodes=""
		for item in doc.items:
			if item.purchase_order:
				if item.item_verified == 0:
					ts_item_details=frappe.get_doc("Item",item.item_code)
					if ts_item_details.barcodes:
						ts_item_barcodes += "•"+item.item_code+'<br>'
		if ts_item_barcodes:
			frappe.throw(_("Below Items Are Not Verified, Please Check It... <br>{0}").format(ts_item_barcodes))

	# Supplier Invoice Amount Validation With Our Invoice
	ts_value=frappe.db.get_single_value("Thirvu Retail Settings","invoice_amount_should_be_matched")
	if ts_value==1:
		ts_difference_amount=""
		if doc.rounded_total:
			if doc.supplier_invoice_amount != doc.rounded_total:
				ts_difference_amount = doc.rounded_total - doc.supplier_invoice_amount
			
			if ts_difference_amount:
				frappe.throw(_("• Supplier Invoice Amount Is Differ From Our Purchase Invoice<br> • Difference Amount Is <b>₹{0}</b> <br> • So,Please Verify It...").format(ts_difference_amount))
