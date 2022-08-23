# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe.utils import nowdate
from frappe.model.document import Document
import json
from datetime import date, timedelta
from erpnext.accounts.utils import now
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
def payment_entry(mode,amount,pending_invoice,company,driver_id):
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
        'driver' :driver_id,
        'mode_of_payment_by_driver' :mode,
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

@frappe.whitelist()
def driver_mode_of_payments(driver_id):
    thirvu_mode_of_payments = frappe.get_list("Thirvu Driver Mode of Payments",{"parent":driver_id},pluck="mode_of_payment")
    return thirvu_mode_of_payments

@frappe.whitelist()
def get_fields_for_denomination(driver_id):
    driver_doc=frappe.get_doc("Driver",driver_id)
    ts_mode_of_payment=[]
    ts_denomination=[]
    for i in driver_doc.thirvu_mode_of_payments:
        ts_mode_of_payment_type=frappe.get_doc("Mode of Payment",i.mode_of_payment)
        if ts_mode_of_payment_type.type != "Cash":
            row = frappe._dict()
            row.update({'ts_type':i.mode_of_payment})
            ts_mode_of_payment.append(row)
        if ts_mode_of_payment_type.type == "Cash":
            amounts = frappe.get_all("Denomination Rupees", pluck = 'amount',order_by = '`amount` desc')
            for i in amounts:
                row = frappe._dict()
                row.update({'currency':i})
                ts_denomination.append(row)
    return ts_denomination,ts_mode_of_payment

@frappe.whitelist()
def create_driver_closing_shift(ts_denomination,driver_name,creation_datetime,driver_id,doc_name):
    driver_closing_shift_grace_amt = frappe.db.get_single_value('Thirvu Retail Settings', 'driver_closing_shift_grace_amount')
    denomination_validation=json.loads(ts_denomination)
    try:
        denomination=denomination_validation["ts_denomination"]
    except:
        denomination=[]
    try:
        ts_mode_of_payment=denomination_validation["ts_mode_of_payment"]
    except:
        ts_mode_of_payment=[]
    denomination_cash=0
    other_cash=0
    payment_reconcilation=[]
    ts_total_count = 0
    expected_denomination_cash = 0
    ts_denomination_and_other_payments_count = len(denomination) + len(ts_mode_of_payment)
    for count in denomination:
        try:
            if count["count"]:
                denomination_cash+=(count['currency'] * count['count'])
        except:
            ts_total_count+=1
    thirvu_mode_of_payments=frappe.get_list("Thirvu Driver Mode of Payments",{"parent":driver_id},pluck="mode_of_payment")
    for modes in thirvu_mode_of_payments:
        amount_type=frappe.db.get_value("Mode of Payment",modes,"type")
        if(amount_type=="Cash"):
            expected_denomination_cash=frappe.db.sql("""select sum(paid_amount) from `tabPayment Entry`
                                            where creation between '{0}' and '{1}' and
                                            driver='{2}' and mode_of_payment_by_driver='{3}' """.format(creation_datetime,now(),driver_id,modes),as_list=1)[0][0]
            if expected_denomination_cash != None:
                row = frappe._dict()
                row.update({'mode_of_payment':modes,
                            "opening_amount":0,
                            "closing_amount":denomination_cash,
                            "expected_amount":expected_denomination_cash,
                            "difference":denomination_cash - expected_denomination_cash})
                payment_reconcilation.append(row)
            else:
                expected_denomination_cash=0
                row = frappe._dict()
                row.update({'mode_of_payment':modes,
                            "opening_amount":0,
                            "closing_amount":denomination_cash,
                            "expected_amount":expected_denomination_cash,
                            "difference":denomination_cash-expected_denomination_cash})
                payment_reconcilation.append(row)
    for type in ts_mode_of_payment:
        try:
            if type["currency"]:
                other_cash+=(type['currency'])
        except:
            ts_total_count+=1
    thirvu_mode_of_payments=frappe.get_list("Thirvu Driver Mode of Payments",{"parent":driver_id},pluck="mode_of_payment")
    for modes in thirvu_mode_of_payments:
        amount_type=frappe.db.get_value("Mode of Payment",modes,"type")
        if(amount_type=="Bank"):
            expected_other_cash=frappe.db.sql("""select sum(paid_amount) from `tabPayment Entry`
                                            where creation between '{0}' and '{1}' and
                                            driver='{2}' and mode_of_payment_by_driver='{3}' and paid_amount IS NOT NULL""".format(creation_datetime,now(),driver_id,modes),as_list=1)[0][0]
            if expected_other_cash != None:
                row = frappe._dict()
                row.update({'mode_of_payment':modes,
                            "opening_amount":0,
                            "closing_amount":other_cash,
                            "expected_amount":expected_other_cash,
                            "difference":other_cash-expected_other_cash})
                payment_reconcilation.append(row)
            else:
                expected_other_cash=0
                row = frappe._dict()
                row.update({'mode_of_payment':modes,
                            "opening_amount":0,
                            "closing_amount":other_cash,
                            "expected_amount":expected_other_cash,
                            "difference":other_cash-expected_other_cash})
                payment_reconcilation.append(row)
    grand_total=denomination_cash+other_cash
    total_difference=0
    driver_doc = frappe.new_doc('Thirvu Driver Closing Shift')
    driver_doc.update({
        'period_start_date':creation_datetime,
        'period_end_date' :now(),
        'posting_date':nowdate(),
        'driver':driver_id,
        'driver_name':driver_name,
        'payment_reconciliation':payment_reconcilation,
        'ts_denomination_counts': denomination,
        'grand_total': grand_total,
        'ts_denomination_total':denomination_cash,
        'reference':doc_name
    })
    driver_doc.insert()
    for data in driver_doc.ts_denomination_counts:
        try:
            if data.count > 0:
                data.total=data.currency * data.count
        except:
            data.total=data.currency * 0
    for rows in driver_doc.payment_reconciliation:
        if rows.difference:total_difference+=rows.difference
        else:total_difference+=0
    if ts_total_count == ts_denomination_and_other_payments_count:
        frappe.msgprint("Your responsible for the difference amount.")
    elif grand_total == 0:
        frappe.msgprint("Your responsible for the difference amount.")
    # elif driver_closing_shift_grace_amt > total_difference:
    #     frappe.msgprint(f"Your responsible for the difference amount of rupees {abs(total_difference)}")
    driver_doc.total_difference = total_difference
    driver_doc.save()
    return total_difference, driver_closing_shift_grace_amt 
    
    
    
    