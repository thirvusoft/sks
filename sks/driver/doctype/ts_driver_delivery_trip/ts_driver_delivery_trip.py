# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import date
class TSDriverDeliveryTrip(Document):
    pass 
@frappe.whitelist()
def get_buttons_data(delivery_trip=None):
    if delivery_trip:
        delivery_stops=[]
        doc = frappe.get_doc("Delivery Trip",delivery_trip)
        for i in doc.delivery_stops:
            s=frappe.get_all("Sales Invoice",fields=['outstanding_amount'],filters ={'name':i.sales_invoice})
            i.amount=s[0].outstanding_amount
            if(i.delivery_status != "Delivered" and i.delivery_status != "Returned"):
                delivery_stops.append(i)
        return doc.delivery_stops
@frappe.whitelist()
def update_values(invoice,fields,value):
    fields = json.loads(fields)
    frappe.db.set_value("Sales Invoice",invoice, 'delivery_status', fields.get('delivery_status'))
    frappe.db.set_value("Sales Invoice",invoice, 'reason', fields.get('reason'))
    frappe.db.set_value("Sales Invoice",invoice, 'time_of_delivery', fields.get('time_of_delivery'))
    frappe.db.commit()
    d = frappe.db.get_all("Delivery Stop",filters={'parent':value,'sales_invoice':invoice})
    doc = frappe.get_doc("Delivery Stop",d[0].name)
    doc.delivery_status=fields.get('delivery_status')
    doc.reason=fields.get('reason')
    doc.time_of_delivery = fields.get('time_of_delivery')
    doc.file_attachment = fields.get('file_attachment')
    doc.save()
    frappe.db.commit()
    return ""

@frappe.whitelist()
def payment_entry(mode,amount,pending_invoice,company):
    customer = frappe.get_value("Sales Invoice",pending_invoice,'customer')
    outstanding = frappe.get_value("Sales Invoice",pending_invoice, 'outstanding_amount')
    ref_date = date.today()
    ref_no = "12315"
    mode_of_payment = frappe.get_doc("Mode of Payment",mode).accounts
    for i in mode_of_payment:
        if(i.company==company):
            acc_paid_to=i.default_account
            break
    try:
        if(acc_paid_to):pass
    except:
        frappe.throw(("Please set Company and Default account for ({0}) mode of payment").format("<a href = /app/mode-of-payment/"+"%20".join(mode.split())+">"+mode+"</a href>"))
    bank_account_type = frappe.db.get_value("Account", acc_paid_to, "account_type")
    if bank_account_type == "Bank":
        if(ref_no == None or ref_date == None):
            frappe.throw("Reference No and Reference Date is mandatory for Bank transaction")
    acc_currency = frappe.db.get_value('Account',acc_paid_to,'account_currency')
    doc = frappe.new_doc('Payment Entry')
    references=[]
    amount1 = float(amount)
    if(amount1 > outstanding):
        return "Unable to create payment entry for {0}".format(pending_invoice), 'red',amount1,outstanding
        
    references.append({
        'reference_doctype':'Sales Invoice',
        'reference_name': pending_invoice,
        'total_amount':amount1,
        'exchange_rate': 1,
        'allocated_amount': amount1
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
        # 'pos_opening_shift_id': opening
    })
    if(bank_account_type == 'Bank'):
        doc.update({
            'reference_no':ref_no,
            'reference_date':ref_date
        })
    doc.insert()
    doc.submit()
    frappe.db.commit()
    return "Payment Entry {0} created for {1}".format(doc.name,pending_invoice),'green'