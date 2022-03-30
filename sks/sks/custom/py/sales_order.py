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
    length_creation_date=len(creation_date)
    if(length_creation_date!=0):
        return item_list, creation_date,item_code
    else:
        return 0

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
def subwarehouse(sub_warehouse=None,company=None):
    item_code=[]
    item_warehouse=[]
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
    for i in range(0,len(bin_data),1):
        item_code.append(bin_data[i]["item_code"])
        item_warehouse.append(bin_data[i]["warehouse"])
    return item_code, item_warehouse

@frappe.whitelist()
def bins(total_item_code=None,subwarehouse_item_codes=None,subwarehouse_item_bins=None,doctype_name=None,document_name=None):
    total_item_code=eval(total_item_code)
    subwarehouse_item_codes=eval(subwarehouse_item_codes)
    subwarehouse_item_bins=eval(subwarehouse_item_bins)
    sales_order_document=frappe.get_doc(doctype_name,document_name)
    for i in range(0,len(subwarehouse_item_codes),1):
        for item in sales_order_document.items:
            if(subwarehouse_item_codes[i]==item.__dict__["item_code"]):
                    frappe.set_value(item.doctype,item.name,"warehouse",subwarehouse_item_bins[i])
    return 0

@frappe.whitelist(allow_guest=True)
def customer_credit_sale(customer):
    doc = frappe.get_list("Sales Invoice",
        filters={"customer":customer,
            "status":('in',('Partly Paid','Unpaid','Overdue','Unpaid and Discounted', 
            'Overdue and Discounted', 'Partly Paid and Discounted')),'docstatus':1},
        fields=['base_paid_amount','name','base_rounded_total','outstanding_amount'])
    pending_invoice={}
    recievable=0
    for i in doc[::-1]:
        if(i['base_paid_amount'] != i['base_rounded_total']):
            pending_invoice[i['name']] = i['outstanding_amount']
    alert_data=""
    html=str("<tr class=clstr><td class=clstd><b><right>" + "Sales Invoice No"  + "</right></b></td><td class=clstd><b><center>" + "&#12288 Outstanding" + "</center></b></td></tr>")
    for i in pending_invoice:
        html+= "<tr class=clstr><td class=clstd><left><a href=/app/sales-invoice/"+str(i)+'>' + str(i) + "</a></left></td><td class=clstd><center> &#12288 &#12288 " + str(pending_invoice[i]) + "</center></td></tr>"
        recievable+=pending_invoice[i]
        alert_data+=str(i)+" with amount "+str(pending_invoice[i])+", "
    alert_data=("Customer: "+str(customer)+" has Unpaid amount of RS."+str(recievable))+" with the credit bills of "+alert_data 
    html = "<html><style> .clstab, .clsth, .clstd { border: 1px solid black; border-collapse: collapse;}   .clsth, .clstd {padding: 15px;} .clstab {width:100%;} </style>" + "<table class=clstab>" + html +"</table>"
    alert_data = alert_data[:len(alert_data)-2]+"."
    return alert_data,pending_invoice,recievable, html