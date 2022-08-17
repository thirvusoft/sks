import frappe
import json
from frappe import _
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
@frappe.whitelist(allow_guest=True)
def payment_entry(amount,mode,customer,pending_invoice,company,ref_no=None,ref_date=None):
	mode_of_payment = frappe.get_doc("Mode of Payment",mode).accounts
	for i in mode_of_payment:
		if(i.company==company):
			acc_paid_to=i.default_account
			break
	try:
		if(acc_paid_to):pass
	except:
		frappe.throw(("Please set Company and Default account for ({0}) mode of payment").format(mode))
	bank_account_type = frappe.db.get_value("Account", acc_paid_to, "account_type")
	if bank_account_type == "Bank":
		if(ref_no == None or ref_date == None):
			frappe.throw("Reference No and Reference Date is mandatory for Bank transaction")
	acc_currency = frappe.db.get_value('Account',acc_paid_to,'account_currency')
	pending_invoice = eval(pending_invoice)
	doc = frappe.new_doc('Payment Entry')
	references=[]
	amount1 = float(amount)
	for i in pending_invoice:
		amount_allocated = 0
		if(amount1 >= pending_invoice[i]):
			amount_allocated = pending_invoice[i]
			amount1 -= pending_invoice[i]
		else:
			amount_allocated=amount1
			amount1 -= amount_allocated
		if(amount_allocated>0):
			references.append({
				'reference_doctype':'Sales Invoice',
				'reference_name': i,
				'total_amount':pending_invoice[i],
				'exchange_rate': 1,
				'allocated_amount': amount_allocated
			})
	doc.update({
		'company':company,
		'payment_type':"Receive",
		'docstatus': 1,
		'mode_of_payment':mode,
		'party_type': 'Customer',
		'party': customer,
		'paid_amount':float(amount),
		'source_exchange_rate':1,
		'references':references,
		'received_amount':float(amount),
		'target_exchange_rate':1,
		'paid_to': acc_paid_to,
		'paid_to_account_currency': acc_currency,
	})
	if(bank_account_type == 'Bank'):
		doc.update({
			'reference_no':ref_no,
			'reference_date':ref_date
		})
	doc.insert()
	doc.submit()
	frappe.db.commit()
	return doc.paid_amount,mode

@frappe.whitelist()
def feed_back_form(doc, action): 
	si=frappe.get_all('Customer Feedback Form', 
			filters={'customer_name': doc.customer},
			fields=['name'])
	
	compliants_dict={}
	compliants=[]
	for i in frappe.get_meta("Customer Feedback Form").fields:
		compliants_dict[i.fieldname]=i.label
		if(i.fieldtype == "Check"):
			compliants.append(i.fieldname)
  
	
	if si:
		cff=frappe.get_doc("Customer Feedback Form", si[0]['name'])
		compliants_list=[]
		feedback1=cff.invoice_no
		feedback2=cff.customer_name
		feedback3=cff.ratings
		for i in compliants:
			if(cff.__dict__[i]==1 and i!="others_check"):
				compliants_list.append("<li>"+compliants_dict[i]+"</li>")
			elif(i=="others_check"):
				if(cff.__dict__[i]==1):
					compliants_list.append("<p>"+cff.others+"</p>")
		
		frappe.msgprint('<b>Rating: </b> '+('⭐'*feedback3)+'<p><b>Feedback: </b> </p><ul>'+" ".join(compliants_list)+'</ul>')


@frappe.whitelist()
def saving_amount(doc,event):
	total_mrp=0
	for row in doc.items:
		total_mrp+=row.mrp*row.qty
	doc.your_savings = total_mrp-doc.rounded_total

@frappe.whitelist()
def billed_by(doc,event):
	if doc.is_pos==1:
		if doc.pos_profile:
			ts_user=frappe.get_value("User",{"name":doc.owner},"full_name")
			doc.billed_by=ts_user

@frappe.whitelist()
def barcode_creation(doc,event):
	if doc.bill_barcode == None:
		doc.bill_barcode=doc.name



@frappe.whitelist()
def delivery_note_to_sales_invoice(data):
	data=json.loads(data)	
	if data["mode_of_delivery"] == "Is Local Delivery":
		dn_doc=frappe.get_list("Delivery Note",{"is_against_sales_invoice":0,"is_local_delivery":1,"status":"To Bill"},pluck="name")
	else:
		dn_doc=frappe.get_list("Delivery Note",{"is_against_sales_invoice":0,"mode_of_delivery":data["mode_of_delivery"],"delivery_day":data["delivery_day"],"status":"To Bill"},pluck="name")
	if dn_doc != []:
		convereted_doc_count=0
		not_converted_doc=""
		for source_name in dn_doc:
			try:
				sales_invoice_doc=(make_sales_invoice(source_name))
				sales_invoice_doc.save()
				dn_new_doc=frappe.get_doc("Delivery Note",source_name)
				dn_new_doc.is_against_sales_invoice = 1
				dn_new_doc.save()
				frappe.db.commit()
				convereted_doc_count+=1
			except:
				not_converted_doc += "•"+source_name+'<br>'

			s_msg=f"No Of Sales Invoive Created :{convereted_doc_count} <br>"
			f_msg=f"Below Delivery Notes Are Not Converted To Sales Invoice :<br>{not_converted_doc}"
			if s_msg != "No Of Sales Invoive Created :0" and not_converted_doc != "":
				msg=s_msg+f_msg
			elif s_msg != "No Of Sales Invoive Created :":
				msg=s_msg
			elif f_msg !="Below Delivery Notes Are Not Converted To Sales Invoice :":
				msg=f_msg
		return msg
	else:
		msg="No Delivery Notes to convert"
		return msg
		  
def mode_of_payment(doc,event):
	try:
		mode_of_payment = doc.payments[0].mode_of_payment
		bank_type= frappe.get_value("Mode of Payment",{"name":mode_of_payment},["type","bank_type"], as_dict=1)
		print(bank_type)
		if bank_type["type"] == "Bank":
			doc.mode_of_payment = bank_type["bank_type"]
		elif bank_type["type"] == "Cash":
			doc.mode_of_payment = bank_type["type"]
	except:
	 	pass