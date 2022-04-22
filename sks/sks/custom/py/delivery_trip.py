import frappe
import json
from datetime import date
@frappe.whitelist()
def get_sales_invoice(territory,date):
    salesorder = frappe.get_all("Sales Order",filters = {"delivery_date":date},pluck = 'name')
    sales_invoice = frappe.get_all("Sales Invoice Item",filters = {"sales_order":["in",salesorder]},pluck = 'parent')
    sales = frappe.get_all("Sales Invoice",fields=['name','customer_address','customer','delivery_status','reason','contact_person','time_of_delivery','paid_amount'],filters ={'territory':territory,'name':['in',sales_invoice]})
    # sales =  frappe.db.sql('''
    # select name as sales_invoice, customer_address as address, customer, delivery_status from `tabSales Invoice` where territory = "{0}" and name in ({1})
    # '''.format(territory,*sales_invoice),as_dict = 1)
    return sales
@frappe.whitelist()
def update_invoice(invoice,fields):
    fields = json.loads(fields)
    frappe.db.set_value("Sales Invoice",invoice, 'delivery_status', fields['delivery_status'])
    frappe.db.set_value("Sales Invoice",invoice, 'reason', fields['reason'])
    frappe.db.set_value("Sales Invoice",invoice, 'time_of_delivery', fields['time_of_delivery'])
    frappe.db.commit()
    return ""

# @frappe.whitelist()
# def payment_entry(mode,amount,pending_invoice,company):
#     customer = frappe.get_value("Sales Invoice",pending_invoice[0],'customer')
#     ref_date = date.today()
#     ref_no = "12315"
#     mode_of_payment = frappe.get_doc("Mode of Payment",mode).accounts
#     for i in mode_of_payment:
#         if(i.company==company):
#             acc_paid_to=i.default_account
#             break
#     try:
#         if(acc_paid_to):pass
#     except:
#         frappe.throw(("Please set Company and Default account for ({0}) mode of payment").format(mode))
#     bank_account_type = frappe.db.get_value("Account", acc_paid_to, "account_type")
#     if bank_account_type == "Bank":
#         if(ref_no == None or ref_date == None):
#             frappe.throw("Reference No and Reference Date is mandatory for Bank transaction")
#     acc_currency = frappe.db.get_value('Account',acc_paid_to,'account_currency')
#     pending_invoice = [pending_invoice]
#     doc = frappe.new_doc('Payment Entry')
#     references=[]
#     amount1 = float(amount)
#     for i in pending_invoice:
#         amount_allocated = 0
#         if(amount1 >= pending_invoice[i]):
#             amount_allocated = pending_invoice[i]
#             amount1 -= pending_invoice[i]
#         else:
#             amount_allocated=amount1
#             amount1 -= amount_allocated
#         if(amount_allocated>0):
#             references.append({
#                 'reference_doctype':'Sales Invoice',
#                 'reference_name': i,
#                 'total_amount':pending_invoice[i],
#                 'exchange_rate': 1,
#                 'allocated_amount': amount_allocated
#             })
#     doc.update({
#         'company':company,
#         'payment_type':"Receive",
#         'docstatus': 1,
#         'mode_of_payment':mode,
#         'party_type': 'Customer',
#         'party': customer,
#         'paid_amount':float(amount),
#         'source_exchange_rate':1,
#         'references':references,
#         'received_amount':float(amount),
#         'target_exchange_rate':1,
#         'paid_to': acc_paid_to,
#         'paid_to_account_currency': acc_currency,
#         # 'pos_opening_shift_id': opening
#     })
#     if(bank_account_type == 'Bank'):
#         doc.update({
#             'reference_no':ref_no,
#             'reference_date':ref_date
#         })
#     doc.insert()
#     doc.submit()
#     frappe.db.commit()
#     return doc.paid_amount, mode





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
        frappe.throw(("Please set Company and Default account for ({0}) mode of payment").format(mode))
    bank_account_type = frappe.db.get_value("Account", acc_paid_to, "account_type")
    if bank_account_type == "Bank":
        if(ref_no == None or ref_date == None):
            frappe.throw("Reference No and Reference Date is mandatory for Bank transaction")
    acc_currency = frappe.db.get_value('Account',acc_paid_to,'account_currency')
    doc = frappe.new_doc('Payment Entry')
    references=[]
    amount1 = float(amount)
    if(amount1 > outstanding):
        frappe.throw("Paid Amount is greater than the Outstanding Amount. ({} > {})".format(amount1,outstanding))
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
    return doc.paid_amount, mode