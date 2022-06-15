import frappe

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

@frappe.whitelist(allow_guest=True)
def payment_entry(amount,mode,customer,pending_invoice,company,opening,ref_no=None,ref_date=None):
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
        'pos_opening_shift_id': opening
    })
    if(bank_account_type == 'Bank'):
        doc.update({
            'reference_no':ref_no,
            'reference_date':ref_date
        })
    doc.insert()
    doc.submit()
    frappe.db.commit()
    if(doc.docstatus == 1):
        pos = frappe.get_doc("POS Awesome Outstanding Amount",opening)
        outstanding={
            'customer': customer,
            'payment_entry': doc.name,
            'mode_of_payment' : mode,
            'date': doc.posting_date,
            'amount': doc.paid_amount
        }
        pos.append('outstanding_amount' ,outstanding )
        pos.save()
        frappe.db.commit()
    return doc.paid_amount, mode



@frappe.whitelist(allow_guest=True)
def customer_transaction_history(customer): 
    from datetime import datetime   
    data = frappe.get_all("Sales Invoice",filters={'docstatus':1,'customer':customer},limit=10)
    item_list={}
    creation_date={}
    today = datetime.now()
    html=""
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
            if(j.item_code == None):
                j.item_code = " "
            if(j.rate in rates):invoice_item.append(str(j.item_name + " (" + j.item_code + ")"))
        if(date.days == 0):creation_date[i['name']] = ['Today']
        else:creation_date[i['name']] = [str(date.days)+" days ago"]
        invoice_item=", ".join(invoice_item)
        html+= "<tr class=clstr>"+"<td class=clstd>"+"<b><a href=/app/sales-invoice/"+i['name']+'>'+i['name']+"</a></b>"+"</td><td class=clstd>"+"&#12288"+invoice_item+"</td>"+"<td class=clstd>"+" &#12288 "+creation_date[i['name']][0]+"</td>"+"</tr>"
        invoice_item=[frappe.bold(i['name'])+":   &#12288"+invoice_item+"&#12288"] 
        item_list[i['name']] = invoice_item
    ic_dict = frappe.db.get_list("Item",fields=['item_code'],filters={'disabled':0})
    ic=[]
    for i in ic_dict:
        ic.append(i['item_code'])
    html = "<html><style> .clstab, .clsth, .clstd { border: 1px solid black; border-collapse: collapse;}   .clsth, .clstd {padding: 10px;} .clstab {width:100%;} </style>" + "<table class=clstab><tr class=clstr><td class=clstd><b>Invoice No</b></td><td class=clstd><b>Items Purchased</b></td><td class=clstd><b>Days ago</b></td><tr>" + html +"</table>"
    return item_list, len(creation_date),ic,html


@frappe.whitelist()
def validate_delivery_type(data,customer):
    data = eval(data)
    if(list(data.values()).count(1) > 1 ):
        frappe.throw("Don't select more than one delivery type")
    elif(list(data.values()).count(1) == 0):
        frappe.throw("Please select atleast one delivery type")
    for i in data:
        if(data[i] == 1):
            mode = i
            break
    # if(data['bus_delivery'] == 1):
    #     bus = frappe.db.get_all('TS Bus Details',fields=['name','destination'])
    #     bus_dict={i['name']:i['destination'] for i in bus}
    #     return bus_dict,mode
    if(data['delivery_pickup'] == 1):
        link = frappe.db.get_all('Dynamic Link',fields=['parent','name'],filters={'link_name':customer,'parenttype':'Contact','parentfield':'links','link_doctype':'Customer'})
        contact = [i['parent'] for i in link]
        # invoice_contact = {}
        cnt = frappe.db.get_list('Contact',fields=['first_name'],filters={'name':['in',contact]})
        cnt_name = [i['first_name'] for i in cnt]
        return contact,mode
    else:
        return [], mode
    
