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
    frappe.errprint(pending_invoice)
    alert_data=""
    for i in pending_invoice:
        recievable+=pending_invoice[i]
        alert_data+=str(i)+" with amount "+str(pending_invoice[i])+", "
    alert_data=("Customer: "+str(customer)+" has Unpaid amount of RS."+str(recievable))+" with the credit bills of "+alert_data 
   # if(recievable>0):frappe.msgprint(alert_data[:len(alert_data)-2]+".")
    

    
    alert_data = alert_data[:len(alert_data)-2]+"."
    
    return alert_data,pending_invoice,recievable

@frappe.whitelist(allow_guest=True)
def payment_entry(amount,mode,customer,pending_invoice,company,ref_no,ref_date):
    mode_of_payment = frappe.get_doc("Mode of Payment",mode).accounts
    frappe.errprint(mode_of_payment)
    for i in mode_of_payment:
        if(i.company==company):
            acc_paid_to=i.default_account
            break
    bank_account_type = frappe.db.get_value("Account", acc_paid_to, "account_type")
    if bank_account_type == "Bank":
        if not ref_no or not ref_date:
            frappe.throw("Reference No and Reference Date is mandatory for Bank transaction11")
    acc_currency = frappe.db.get_value('Account',acc_paid_to,'account_currency')
    pending_invoice = eval(pending_invoice)
    frappe.errprint("Reached")
    doc = frappe.new_doc('Payment Entry')
    references=[]
    amount1 = int(amount)
    for i in pending_invoice:
        amount_allocated = 0
        frappe.errprint(str(amount1)+" "+str(pending_invoice[i]))
        if(amount1 >= pending_invoice[i]):
            amount_allocated = pending_invoice[i]
            amount1 -= pending_invoice[i]
        else:
            #amount1=pending_invoice[i]
            amount_allocated=amount1
            amount1 -= amount_allocated
        frappe.errprint(str(amount1)+" "+str(pending_invoice[i]))
        frappe.errprint(i)
        if(amount_allocated>0):
            references.append({
                'reference_doctype':'Sales Invoice',
                'reference_name': i,
                'total_amount':pending_invoice[i],
                'exchange_rate': 1,
                'allocated_amount': amount_allocated
            })
    frappe.errprint(references)
    doc.update({
        'company':company,
        'payment_type':"Receive",
        'docstatus': 1,
        'mode_of_payment':mode,
        'party_type': 'Customer',
        'party': customer,
        'paid_amount':int(amount),
        'source_exchange_rate':1,
        'references':references,
        'received_amount':int(amount),
        'target_exchange_rate':1,
        'paid_to': acc_paid_to,
        'paid_to_account_currency': acc_currency
    })
    frappe.errprint("doc is printing below.....")
    frappe.errprint(doc.difference_amount)
    doc.insert()
    doc.submit()
    frappe.db.commit()
    frappe.errprint(doc.__dict__)
    return doc



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
        frappe.errprint(rates)
        for j in items:
            if(j.rate in rates):invoice_item.append(j.item_name)
        if(date.days == 0):creation_date[i['name']] = ['Today']
        else:creation_date[i['name']] = [str(date.days)+" days ago"]
        invoice_item=", ".join(invoice_item)
        invoice_item=[frappe.bold(i['name'])+":   &#12288"+invoice_item+"&#12288"]   
        item_list[i['name']] = invoice_item
    frappe.errprint("In Py")
    frappe.errprint(item_list)
    frappe.errprint(creation_date)
    return item_list, creation_date
