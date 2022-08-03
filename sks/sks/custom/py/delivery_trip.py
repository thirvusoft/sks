import frappe
import json
from datetime import date
from frappe.desk.form import assign_to

@frappe.whitelist()
def update_invoice(invoice,fields):
    fields = json.loads(fields)
    frappe.db.set_value("Sales Invoice",invoice, 'delivery_status', fields.get('delivery_status'))
    frappe.db.set_value("Sales Invoice",invoice, 'reason', fields.get('reason'))
    frappe.db.set_value("Sales Invoice",invoice, 'time_of_delivery', fields.get('time_of_delivery'))
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

@frappe.whitelist()
def get_customer_territory():
    return frappe.get_all("Territory",filters={'is_group':0},pluck="name") 

@frappe.whitelist()
def get_condition_from_dialog(data):
    data = json.loads(data)
    filter={'docstatus':1}
    data_key = list(data.keys())
    if('customer' in data_key):
        filter['customer'] = data['customer']
    if('day' in data_key):
        filter['delivery_day'] = (data['day'])
    if('territory' in data_key):
        filter['territory'] = ['in', data['territory']]
    sales_order = get_sales_order(filter)

    filter1 = {}
    sales_invoice =[]
    if(len(sales_order)):
        filter1['sales_order'] = ['in',sales_order]
        if('invoice' in data_key):
            filter1['parent'] = data['invoice']
        # filter1 = {'delivery_status': ['not in', ['Delivered', 'Returned']]}
        sales_invoice = get_sales_invoice(filter1, 'Sales Invoice Item','parent')
    if(len(sales_invoice)):
        if('outstanding' in data_key):
            filter1['outstanding_amount'] = ['>=', data['outstanding']]
            filter1['name'] = ['in', sales_invoice]
            filter1['docstatus'] = 1
            filter1['delivery_status']= ['not in', ['Delivered', 'Returned','Out to Delivery']]
            sales_invoice = get_sales_invoice(filter1,"Sales Invoice",'name')
            return get_sales_invoice_details(sales_invoice)
    else:
        frappe.throw("Not any Sales Invoice matched for this condition")

def get_sales_order(filter):
    return frappe.get_all("Sales Order",filters=filter,pluck="name")

def get_sales_invoice(filter,doctype,name):
    return frappe.get_all(doctype, filters= filter, pluck = name)

def get_sales_invoice_details(sales_invoice):
    return frappe.get_all("Sales Invoice",fields=['name','customer_address','customer','delivery_status','reason','contact_person','time_of_delivery','rounded_total','outstanding_amount'],filters ={'name':['in',sales_invoice],'delivery_status':['not in', ['Delivered', 'Returned']]})
def assign_to_driver(del_trip,a):

    # Updation of Out to Delivery Status
    for i in del_trip.delivery_stops:
        sales_inv_doc = frappe.get_doc('Sales Invoice',i.sales_invoice)
        sales_inv_doc.delivery_status = 'Out to Delivery'
        sales_inv_doc.save()

    allow=0
    row=0
    for i in del_trip.delivery_stops:
        if(i.delivery_status != "Delivered"):
            allow=1
    if(allow==1):
        doc = frappe.new_doc('TS Driver Delivery Trip')
        del_trip_doc = frappe.get_doc('Delivery Trip', del_trip.name)
        doc.update({
            'driver_id':del_trip_doc.driver,
            'driver': del_trip_doc.driver_name,
            'vehicle': del_trip_doc.vehicle,
            'delivery_trip': del_trip_doc.name,
            'company': del_trip_doc.company,
            'status': "Open"
        })
        doc.insert(ignore_permissions=True)
        if(del_trip.driver):
            assign_to.add(
                dict(
                    assign_to=[del_trip.user_id],
                    doctype="TS Driver Delivery Trip",
                    name=doc.name,
                    notify=True,
                )
            )
        return doc
    else:
        frappe.throw("All the Sales Invoice are Delivered")

def update_sales_invoice(doc,event):
    # Updation of Hold Status
    for i in doc.delivery_stops:
        sales_inv_doc = frappe.get_doc('Sales Invoice',i.sales_invoice)
        sales_inv_doc.delivery_status = 'Hold'
        sales_inv_doc.save()