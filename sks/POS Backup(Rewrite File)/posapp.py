# Copyright (c) 2020, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataclasses import field
import json
import frappe
from frappe.utils import nowdate, flt, cstr
from frappe import _
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from erpnext.stock.get_item_details import get_item_details
from erpnext.accounts.doctype.pos_profile.pos_profile import get_item_groups
from frappe.utils.background_jobs import enqueue
from erpnext.accounts.party import get_party_bank_account
from erpnext.stock.doctype.batch.batch import get_batch_no, get_batch_qty, set_batch_nos
from erpnext.accounts.doctype.payment_request.payment_request import (
    get_gateway_details,
    get_dummy_message,
    get_existing_payment_request_amount,
)
from erpnext.controllers.accounts_controller import add_taxes_from_tax_template
from erpnext.accounts.doctype.loyalty_program.loyalty_program import (
    get_loyalty_program_details_with_points,
)
from posawesome.posawesome.doctype.pos_coupon.pos_coupon import check_coupon_code

# from posawesome import console


@frappe.whitelist()
def get_opening_dialog_data():
    data = {}
    data["companys"] = frappe.get_list("Company", limit_page_length=0, order_by="name")
    data["pos_profiles_data"] = frappe.get_list(
        "POS Profile",
        filters={"disabled": 0},
        fields=["name", "company"],
        limit_page_length=0,
        order_by="name",
    )

    pos_profiles_list = []
    for i in data["pos_profiles_data"]:
        pos_profiles_list.append(i.name)

    payment_method_table = (
        "POS Payment Method" if get_version() == 13 else "Sales Invoice Payment"
    )
    data["payments_method"] = frappe.get_list(
        payment_method_table,
        filters={"parent": ["in", pos_profiles_list]},
        fields=["*"],
        limit_page_length=0,
        order_by="parent",
    )

    return data


@frappe.whitelist()
def create_opening_voucher(pos_profile, company, balance_details):
    balance_details = json.loads(balance_details)

    new_pos_opening = frappe.get_doc(
        {
            "doctype": "POS Opening Shift",
            "period_start_date": frappe.utils.get_datetime(),
            "posting_date": frappe.utils.getdate(),
            "user": frappe.session.user,
            "pos_profile": pos_profile,
            "company": company,
        }
    )
    new_pos_opening.set("balance_details", balance_details)
    new_pos_opening.submit()

    data = {}
    data["pos_opening_shift"] = new_pos_opening.as_dict()
    update_opening_shift_data(data, new_pos_opening.pos_profile)

    #code start
    pos=frappe.new_doc("POS Awesome Outstanding Amount")
    pos.update({
        'pos_opening_shift' : new_pos_opening.name,
        'pos_profile' : pos_profile,
        'posting_date' : frappe.utils.getdate(),
        'cashier' : frappe.session.user,
        'docstatus' : 0
    })
    pos.insert()
    frappe.db.commit()
    #code end

    return data


@frappe.whitelist()
def check_opening_shift(user):
    open_vouchers = frappe.db.get_all(
        "POS Opening Shift",
        filters={
            "user": user,
            "pos_closing_shift": ["in", ["", None]],
            "docstatus": 1,
            "status": "Open",
        },
        fields=["name", "pos_profile"],
        order_by="period_start_date desc",
    )
    data = ""
    if len(open_vouchers) > 0:
        data = {}
        data["pos_opening_shift"] = frappe.get_doc(
            "POS Opening Shift", open_vouchers[0]["name"]
        )
        update_opening_shift_data(data, open_vouchers[0]["pos_profile"])
    return data


def update_opening_shift_data(data, pos_profile):
    data["pos_profile"] = frappe.get_doc("POS Profile", pos_profile)
    data["company"] = frappe.get_doc("Company", data["pos_profile"].company)
    allow_negative_stock = frappe.get_value(
        "Stock Settings", None, "allow_negative_stock"
    )
    data["stock_settings"] = {}
    data["stock_settings"].update({"allow_negative_stock": allow_negative_stock})


@frappe.whitelist()
def get_items(pos_profile, price_list=None):
    pos_profile = json.loads(pos_profile)
    if not price_list:
        price_list = pos_profile.get("selling_price_list")
    condition = ""
    condition += get_item_group_condition(pos_profile.get("name"))
    if not pos_profile.get("posa_show_template_items"):
        condition += " AND has_variants = 0"

    result = []

    items_data = frappe.db.sql(
        """
        SELECT
            name AS item_code,
            item_name,
            description,
            stock_uom,
            image,
            is_stock_item,
            has_variants,
            variant_of,
            item_group,
            idx as idx,
            has_batch_no,
            has_serial_no,
            max_discount,
            brand
        FROM
            `tabItem`
        WHERE
            disabled = 0
                AND is_sales_item = 1
                AND is_fixed_asset = 0
                {0}
        ORDER BY
            name asc
            """.format(
            condition
        ),
        as_dict=1,
    )
    #code start
    sub_warehouses=[pos_profile.get('warehouse')]

    ware_house=[]  
    while(True):
        for i in sub_warehouses:
            data = frappe.get_all("Warehouse",fields=['name','is_group','parent_warehouse'],filters={'parent_warehouse':i,'company':pos_profile.get('company')})
            for i in data:
                if(i.is_group == 0):ware_house.append(i.name)
                else:sub_warehouses.append(i.name)
            data = frappe.get_all("Warehouse",fields=['name','is_group','parent_warehouse'],filters={'parent_warehouse':pos_profile.get('warehouse'),'company':pos_profile.get('company')})
        sub_warehouses=[]
        if(len(sub_warehouses) == 0):
            break
    if(len(ware_house) == 0):ware_house.append(pos_profile.get("warehouse"))
    bin_data = frappe.get_all("Bin",fields=['item_code','actual_qty','warehouse'],filters={'actual_qty':('>',0),'warehouse':('in',ware_house)})
    item_warehouse={i['item_code']:i['warehouse'] for i in bin_data}
    items=item_warehouse.keys()
    items_data1=[]
    for i in range(len(items_data)):
        if(items_data[i].item_code in items):
            items_data[i]['warehouse']=item_warehouse[items_data[i].item_code]
            items_data[i]['actual_qty']= get_stock_availability(items_data[i].item_code,item_warehouse[items_data[i].item_code])
            items_data1.append(items_data[i])
    items_data=items_data1
    #code end


    if items_data:
        items = [d.item_code for d in items_data]
        item_prices_data = frappe.get_all(
            "Item Price",
            fields=["item_code", "price_list_rate", "currency", "uom"],
            filters={
                "price_list": price_list,
                "item_code": ["in", items],
                "currency": pos_profile.get("currency"),
                "selling": 1,
            },
        )

        item_prices = {}
        for d in item_prices_data:
            item_prices.setdefault(d.item_code, {})
            item_prices[d.item_code][d.get("uom") or "None"] = d  
        i=0
        for item in items_data:
            item_code = item.item_code
            item_wh=item.warehouse
            item_price = {}
            if item_prices.get(item_code):
                item_price = (
                    item_prices.get(item_code).get(item.stock_uom)
                    or item_prices.get(item_code).get("None")
                    or {}
                )
            item_barcode = frappe.get_all(
                "Item Barcode",
                filters={"parent": item_code},
                fields=["barcode", "posa_uom"],
            )
            serial_no_data = []
            if pos_profile.get("posa_search_serial_no"):
                serial_no_data = frappe.get_all(
                    "Serial No",
                    filters={"item_code": item_code, "status": "Active"},
                    fields=["name as serial_no"],
                )
            item_stock_qty = 0
            if pos_profile.get("posa_display_items_in_stock"):
                item_stock_qty = get_stock_availability(
                    item_code, item_wh
                )
                #items_data[i]['actual_qty']=item_stock_qty
            #else:
                #items_data[i]['actual_qty']=0
            attributes = ""
            if pos_profile.get("posa_show_template_items") and item.has_variants:
                attributes = get_item_attributes(item.item_code)
            item_attributes = ""
            if pos_profile.get("posa_show_template_items") and item.variant_of:
                item_attributes = frappe.get_all(
                    "Item Variant Attribute",
                    fields=["attribute", "attribute_value"],
                    filters={"parent": item.item_code, "parentfield": "attributes"},
                )
            if pos_profile.get("posa_display_items_in_stock") and (
                not item_stock_qty or item_stock_qty < 0
            ):
                pass
            else:
                row = {}
                row.update(item)
                row.update(
                    {
                        "rate": item_price.get("price_list_rate") or 0,
                        "currency": item_price.get("currency")
                        or pos_profile.get("currency"),
                        "item_barcode": item_barcode or [],
                        "actual_qty": item_stock_qty,
                        "serial_no_data": serial_no_data or [],
                        "attributes": attributes or "",
                        "item_attributes": item_attributes or ""
                    }
                )
                result.append(row)
            i+=1  
    return result




@frappe.whitelist()
def customer_link_details():
    c_group=frappe.get_all("Customer Group", pluck='name')
    c_territory=frappe.get_all("Territory",pluck='name')
    citys=frappe.get_all("Territory",{'is_group':1},pluck='name')
    return c_group, c_territory, citys


def get_item_group_condition(pos_profile):
    cond = "and 1=1"
    item_groups = get_item_groups(pos_profile)
    if item_groups:
        cond = "and item_group in (%s)" % (", ".join(["%s"] * len(item_groups)))

    return cond % tuple(item_groups)


def get_root_of(doctype):
    """Get root element of a DocType with a tree structure"""
    result = frappe.db.sql(
        """select t1.name from `tab{0}` t1 where
		(select count(*) from `tab{1}` t2 where
			t2.lft < t1.lft and t2.rgt > t1.rgt) = 0
		and t1.rgt > t1.lft""".format(
            doctype, doctype
        )
    )
    return result[0][0] if result else None


@frappe.whitelist()
def get_items_groups():
    return frappe.db.sql(
        """
        select name 
        from `tabItem Group`
        where is_group = 0
        order by name
        LIMIT 0, 200 """,
        as_dict=1,
    )


def get_customer_groups(pos_profile):
    customer_groups = []
    if pos_profile.get("customer_groups"):
        # Get items based on the item groups defined in the POS profile
        for data in pos_profile.get("customer_groups"):
            customer_groups.extend(
                [
                    "%s" % frappe.db.escape(d.get("name"))
                    for d in get_child_nodes(
                        "Customer Group", data.get("customer_group")
                    )
                ]
            )

    return list(set(customer_groups))


def get_child_nodes(group_type, root):
    lft, rgt = frappe.db.get_value(group_type, root, ["lft", "rgt"])
    return frappe.db.sql(
        """ Select name, lft, rgt from `tab{tab}` where
			lft >= {lft} and rgt <= {rgt} order by lft""".format(
            tab=group_type, lft=lft, rgt=rgt
        ),
        as_dict=1,
    )


def get_customer_group_condition(pos_profile):
    cond = "cust.disabled = 0"
    customer_groups = get_customer_groups(pos_profile)
    if customer_groups:
        cond = " customer_group in (%s)" % (", ".join(["%s"] * len(customer_groups)))

    return cond % tuple(customer_groups)


@frappe.whitelist()
def get_customer_names(pos_profile):
    pos_profile = json.loads(pos_profile)
    condition = ""
    condition += get_customer_group_condition(pos_profile)
    customers = frappe.db.sql(
        """
        SELECT cust.name as name, cust.mobile_no as mobile_no, cust.email_id as email_id, cust.tax_id as tax_id, cust.customer_name as customer_name,
        addr.phone as phone1,  
        addr.address_line1 as primary_address, addr.name as addrname
        FROM `tabCustomer` as cust
        left outer join `tabDynamic Link` as link on cust.name = link.link_name
        left outer join `tabAddress` as addr on addr.name = link.parent
        WHERE {0}
        ORDER by cust.name
        """.format(
            condition
        ),
        as_dict=1,
    )
    return customers


@frappe.whitelist()
def update_invoice(data):
    data = json.loads(data)
    if data.get("name"):
        invoice_doc = frappe.get_doc("Sales Invoice", data.get("name"))
        invoice_doc.update(data)
    else:
        invoice_doc = frappe.get_doc(data)


    invoice_doc.flags.ignore_permissions = True
    frappe.flags.ignore_account_permission = True
    if invoice_doc.is_return and invoice_doc.return_against:
        ref_doc = frappe.get_doc(invoice_doc.doctype, invoice_doc.return_against)
        if not ref_doc.update_stock:
            invoice_doc.update_stock = 0

    for item in invoice_doc.items:
        add_taxes_from_tax_template(item, invoice_doc)
    if frappe.get_value("POS Profile", invoice_doc.pos_profile, "posa_tax_inclusive"):
        if invoice_doc.get("taxes"):
            for tax in invoice_doc.taxes:
                tax.included_in_print_rate = 1
    invoice_doc.save()
    ts_settings = frappe.get_value("Thirvu Retail Settings",'Thirvu Retail Settings','allow_display_feedback_required_option')
    feedback_required = frappe.get_value("Customer", invoice_doc.customer, 'feedback_required')
    return invoice_doc, ts_settings, feedback_required


@frappe.whitelist()
def submit_invoice(invoice, data):
    data = json.loads(data)
    invoice = json.loads(invoice)
    invoice_doc = frappe.get_doc("Sales Invoice", invoice.get("name"))
    invoice_doc.update(invoice)
    if invoice.get("posa_delivery_date"):
        invoice_doc.update_stock = 0
    mop_cash_list = [
        i.mode_of_payment
        for i in invoice_doc.payments
        if "cash" in i.mode_of_payment.lower() and i.type == "Cash"
    ]
    if len(mop_cash_list) > 0:
        cash_account = get_bank_cash_account(mop_cash_list[0], invoice_doc.company)
    else:
        cash_account = {
            "account": frappe.get_value(
                "Company", invoice_doc.company, "default_cash_account"
            )
        }

    # creating advance payment
    if data.get("credit_change"):
        advance_payment_entry = frappe.get_doc(
            {
                "doctype": "Payment Entry",
                "mode_of_payment": "Cash",
                "paid_to": cash_account["account"],
                "payment_type": "Receive",
                "party_type": "Customer",
                "party": invoice_doc.get("customer"),
                "paid_amount": invoice_doc.get("credit_change"),
                "received_amount": invoice_doc.get("credit_change"),
                "company": invoice_doc.get("company"),
            }
        )

        advance_payment_entry.flags.ignore_permissions = True
        frappe.flags.ignore_account_permission = True
        advance_payment_entry.save()
        advance_payment_entry.submit()

    # calculating cash
    total_cash = 0
    if data.get("redeemed_customer_credit"):
        total_cash = invoice_doc.total - float(data.get("redeemed_customer_credit"))

    is_payment_entry = 0
    if data.get("redeemed_customer_credit"):
        for row in data.get("customer_credit_dict"):
            if row["type"] == "Advance" and row["credit_to_redeem"]:
                advance = frappe.get_doc("Payment Entry", row["credit_origin"])

                advance_payment = {
                    "reference_type": "Payment Entry",
                    "reference_name": advance.name,
                    "remarks": advance.remarks,
                    "advance_amount": advance.unallocated_amount,
                    "allocated_amount": row["credit_to_redeem"],
                }

                invoice_doc.append("advances", advance_payment)
                invoice_doc.is_pos = 0
                is_payment_entry = 1

    payments = []

    if data.get("is_cashback") and not is_payment_entry:
        for payment in invoice.get("payments"):
            for i in invoice_doc.payments:
                if i.mode_of_payment == payment["mode_of_payment"]:
                    i.amount = payment["amount"]
                    i.base_amount = 0
                    if i.amount:
                        payments.append(i)
                    break

        if len(payments) == 0 and not invoice_doc.is_return and invoice_doc.is_pos:
            payments = [invoice_doc.payments[0]]
    else:
        invoice_doc.is_pos = 0

    invoice_doc.payments = payments
    if frappe.get_value("POS Profile", invoice_doc.pos_profile, "posa_auto_set_batch"):
        set_batch_nos(invoice_doc, "warehouse", throw=True)
    set_batch_nos_for_bundels(invoice_doc, "warehouse", throw=True)
    invoice_doc.due_date = data.get("due_date")
    invoice_doc.flags.ignore_permissions = True
    frappe.flags.ignore_account_permission = True
    invoice_doc.posa_is_printed = 1
    invoice_doc.save()
    invoice_doc.docstatus = 1
    invoice_doc.update_stock = 1
    if frappe.get_value(
        "POS Profile",
        invoice_doc.pos_profile,
        "posa_allow_submissions_in_background_job",
    ):
        invoices_list = frappe.get_all(
            "Sales Invoice",
            filters={
                "posa_pos_opening_shift": invoice_doc.posa_pos_opening_shift,
                "docstatus": 0,
                "posa_is_printed": 1,
            },
        )
        for invoice in invoices_list:
            enqueue(
                method=submit_in_background_job,
                queue="short",
                timeout=1000,
                is_async=True,
                kwargs={
                    "invoice": invoice.name,
                    "data": data,
                    "is_payment_entry": is_payment_entry,
                    "total_cash": total_cash,
                    "cash_account": cash_account,
                },
            )
    else:
        invoice_doc.submit()
        frappe.db.commit()
        redeeming_customer_credit(
            invoice_doc, data, is_payment_entry, total_cash, cash_account
        )

    return {"name": invoice_doc.name, "status": invoice_doc.docstatus}


def set_batch_nos_for_bundels(doc, warehouse_field, throw=False):
    """Automatically select `batch_no` for outgoing items in item table"""
    for d in doc.packed_items:
        qty = d.get("stock_qty") or d.get("transfer_qty") or d.get("qty") or 0
        has_batch_no = frappe.db.get_value("Item", d.item_code, "has_batch_no")
        warehouse = d.get(warehouse_field, None)
        if has_batch_no and warehouse and qty > 0:
            if not d.batch_no:
                d.batch_no = get_batch_no(
                    d.item_code, warehouse, qty, throw, d.serial_no
                )
            else:
                batch_qty = get_batch_qty(batch_no=d.batch_no, warehouse=warehouse)
                if flt(batch_qty, d.precision("qty")) < flt(qty, d.precision("qty")):
                    frappe.throw(
                        _(
                            "Row #{0}: The batch {1} has only {2} qty. Please select another batch which has {3} qty available or split the row into multiple rows, to deliver/issue from multiple batches"
                        ).format(d.idx, d.batch_no, batch_qty, qty)
                    )


def redeeming_customer_credit(
    invoice_doc, data, is_payment_entry, total_cash, cash_account
):
    # redeeming customer credit with journal voucher
    if data.get("redeemed_customer_credit"):
        cost_center = frappe.get_value(
            "POS Profile", invoice_doc.pos_profile, "cost_center"
        )
        if not cost_center:
            cost_center = frappe.get_value(
                "Company", invoice_doc.company, "cost_center"
            )
        if not cost_center:
            frappe.throw(
                _("Cost Center is not set in pos profile {}").format(
                    invoice_doc.pos_profile
                )
            )
        for row in data.get("customer_credit_dict"):
            if row["type"] == "Invoice" and row["credit_to_redeem"]:
                outstanding_invoice = frappe.get_doc(
                    "Sales Invoice", row["credit_origin"]
                )

                jv_doc = frappe.get_doc(
                    {
                        "doctype": "Journal Entry",
                        "voucher_type": "Journal Entry",
                        "posting_date": nowdate(),
                        "company": invoice_doc.company,
                    }
                )

                jv_debit_entry = {
                    "account": outstanding_invoice.debit_to,
                    "party_type": "Customer",
                    "party": invoice_doc.customer,
                    "reference_type": "Sales Invoice",
                    "reference_name": outstanding_invoice.name,
                    "debit_in_account_currency": row["credit_to_redeem"],
                    "cost_center": cost_center,
                }

                jv_credit_entry = {
                    "account": invoice_doc.debit_to,
                    "party_type": "Customer",
                    "party": invoice_doc.customer,
                    "reference_type": "Sales Invoice",
                    "reference_name": invoice_doc.name,
                    "credit_in_account_currency": row["credit_to_redeem"],
                    "cost_center": cost_center,
                }

                jv_doc.append("accounts", jv_debit_entry)
                jv_doc.append("accounts", jv_credit_entry)

                jv_doc.flags.ignore_permissions = True
                frappe.flags.ignore_account_permission = True
                jv_doc.set_missing_values()
                jv_doc.save()
                jv_doc.submit()

    if is_payment_entry and total_cash > 0:
        payment_entry_doc = frappe.get_doc(
            {
                "doctype": "Payment Entry",
                "posting_date": nowdate(),
                "payment_type": "Receive",
                "party_type": "Customer",
                "party": invoice_doc.customer,
                "paid_amount": total_cash,
                "received_amount": total_cash,
                "paid_from": invoice_doc.debit_to,
                "paid_to": cash_account["account"],
                "company": invoice_doc.company,
            }
        )

        payment_reference = {
            "allocated_amount": total_cash,
            "due_date": data.get("due_date"),
            "outstanding_amount": total_cash,
            "reference_doctype": "Sales Invoice",
            "reference_name": invoice_doc.name,
            "total_amount": total_cash,
        }

        payment_entry_doc.append("references", payment_reference)
        payment_entry_doc.flags.ignore_permissions = True
        frappe.flags.ignore_account_permission = True
        payment_entry_doc.save()
        payment_entry_doc.submit()


def submit_in_background_job(kwargs):
    invoice = kwargs.get("invoice")
    invoice_doc = kwargs.get("invoice_doc")
    data = kwargs.get("data")
    is_payment_entry = kwargs.get("is_payment_entry")
    total_cash = kwargs.get("total_cash")
    cash_account = kwargs.get("cash_account")

    invoice_doc = frappe.get_doc("Sales Invoice", invoice)
    invoice_doc.submit()
    redeeming_customer_credit(
        invoice_doc, data, is_payment_entry, total_cash, cash_account
    )


@frappe.whitelist()
def get_available_credit(customer, company):
    total_credit = []

    outstanding_invoices = frappe.get_all(
        "Sales Invoice",
        {
            "outstanding_amount": ["<", 0],
            "docstatus": 1,
            "is_return": 0,
            "customer": customer,
            "company": company,
        },
        ["name", "outstanding_amount"],
    )

    for row in outstanding_invoices:
        outstanding_amount = -(row.outstanding_amount)
        row = {
            "type": "Invoice",
            "credit_origin": row.name,
            "total_credit": outstanding_amount,
            "credit_to_redeem": 0,
        }

        total_credit.append(row)

    advances = frappe.get_all(
        "Payment Entry",
        {
            "unallocated_amount": [">", 0],
            "party_type": "Customer",
            "party": customer,
            "company": company,
        },
        ["name", "unallocated_amount"],
    )

    for row in advances:
        row = {
            "type": "Advance",
            "credit_origin": row.name,
            "total_credit": row.unallocated_amount,
            "credit_to_redeem": 0,
        }

        total_credit.append(row)

    return total_credit


@frappe.whitelist()
def get_draft_invoices(pos_opening_shift):
    invoices_list = frappe.get_list(
        "Sales Invoice",
        filters={
            "posa_pos_opening_shift": pos_opening_shift,
            "docstatus": 0,
            "posa_is_printed": 0,
        },
        fields=["name"],
        limit_page_length=0,
        order_by="customer",
    )
    data = []
    for invoice in invoices_list:
        data.append(frappe.get_doc("Sales Invoice", invoice["name"]))
    return data


@frappe.whitelist()
def delete_invoice(invoice):
    if frappe.get_value("Sales Invoice", invoice, "posa_is_printed"):
        frappe.throw(_("This invoice {0} cannot be deleted").format(invoice))
    frappe.delete_doc("Sales Invoice", invoice, force=1)
    return _("Invoice {0} Deleted").format(invoice)


@frappe.whitelist()
def get_items_details(pos_profile, items_data):
    pos_profile = json.loads(pos_profile)
    items_data = json.loads(items_data)
    # warehouse = pos_profile.get("warehouse")
    result = []
    if len(items_data) > 0:
        for item in items_data:
            warehouse = item.get('warehouse')
            item_code = item.get("item_code")
            item_stock_qty = item.get('actual_qty')
            has_batch_no, has_serial_no = frappe.get_value(
                "Item", item_code, ["has_batch_no", "has_serial_no"]
            )

            uoms = frappe.get_all(
                "UOM Conversion Detail",
                filters={"parent": item_code},
                fields=["uom", "conversion_factor"],
            )

            serial_no_data = frappe.get_all(
                "Serial No",
                filters={"item_code": item_code, "status": "Active"},
                fields=["name as serial_no"],
            )

            batch_no_data = []
            from erpnext.stock.doctype.batch.batch import get_batch_qty

            batch_list = get_batch_qty(warehouse=warehouse, item_code=item_code)

            if batch_list:
                for batch in batch_list:
                    if batch.qty > 0 and batch.batch_no:
                        batch_doc = frappe.get_doc("Batch", batch.batch_no)
                        if (
                            str(batch_doc.expiry_date) > str(nowdate())
                            or batch_doc.expiry_date in ["", None]
                        ) and batch_doc.disabled == 0:
                            batch_no_data.append(
                                {
                                    "batch_no": batch.batch_no,
                                    "batch_qty": batch.qty,
                                    "expiry_date": batch_doc.expiry_date,
                                    "btach_price": batch_doc.posa_btach_price,
                                }
                            )

            row = {}
            row.update(item)
            row.update(
                {
                    "item_uoms": uoms or [],
                    "serial_no_data": serial_no_data or [],
                    "batch_no_data": batch_no_data or [],
                    "actual_qty": item_stock_qty or 0,
                    "has_batch_no": has_batch_no,
                    "has_serial_no": has_serial_no,
                }
            )

            result.append(row)

    return result


@frappe.whitelist()
def get_item_detail(item, doc=None, warehouse=None, price_list=None):
    item = json.loads(item)
    item_code = item.get("item_code")
    if warehouse and item.get("has_batch_no") and not item.get("batch_no"):
        item["batch_no"] = get_batch_no(
            item_code, warehouse, item.get("qty"), False, item.get("d")
        )
    item["selling_price_list"] = price_list
    max_discount = frappe.get_value("Item", item_code, "max_discount")
    res = get_item_details(
        item,
        doc,
        overwrite_warehouse=False,
    )
    
    if item.get("is_stock_item") and warehouse:
        res["actual_qty"] = get_stock_availability(item_code, warehouse)
    res["max_discount"] = max_discount
    return res


def get_stock_availability(item_code, warehouse):
    latest_sle = frappe.db.sql(
        """select qty_after_transaction
		from `tabStock Ledger Entry`
		where item_code = %s and warehouse = %s
		order by posting_date desc, posting_time desc
		limit 1""",
        (item_code, warehouse),
        as_dict=1,
    )

    sle_qty = latest_sle[0].qty_after_transaction or 0 if latest_sle else 0
    return sle_qty


@frappe.whitelist()
def create_customer(
          customer_name,
          mobile1,
          address1,
          address2,
          area,
          city,
          c_group,
 ):
    if not frappe.db.exists("Customer", {"customer_name": customer_name}):
        customer = frappe.get_doc(
            {
                "doctype": "Customer",
                "customer_name": customer_name,
                "mobile_no": mobile1,
                "territory": area,
                "customer_group": c_group,    
            }
        )

        customer.save(ignore_permissions=True)
        if(address1 and mobile1 and city):
            address = frappe.new_doc("Address")
            reference = [{
                'link_doctype': 'Customer',
                'link_name' : customer.name,
                'link_title': customer.name
            }]
            address.update({
                'address_title': customer.name,
                'phone': mobile1,
                'city': city,
                'address_line1': address1,
                'address_line2': address2,
                'links': reference
            })
            address.save(ignore_permissions=True)
            contact = frappe.get_all("Contact Phone", filters={'is_primary_mobile_no':1,'phone':mobile1},pluck='parent')
            if(len(contact)):
                customer.customer_primary_contact = contact[0]
                customer.save(ignore_permissions=True)
        
        return customer
    else:
        return f"Company {customer_name} already Exists."


@frappe.whitelist()
def get_items_from_barcode(selling_price_list, currency, barcode):
    search_item = frappe.get_all(
        "Item Barcode",
        filters={"barcode": barcode},
        fields=["parent", "barcode", "posa_uom"],
    )
    if len(search_item) == 0:
        return ""
    item_code = search_item[0].parent
    item_list = frappe.get_all(
        "Item",
        filters={"name": item_code},
        fields=[
            "name",
            "item_name",
            "description",
            "stock_uom",
            "image",
            "is_stock_item",
            "has_variants",
            "variant_of",
            "item_group",
            "has_batch_no",
            "has_serial_no",
        ],
    )

    if item_list[0]:
        item = item_list[0]
        filters = {"price_list": selling_price_list, "item_code": item_code}
        prices_with_uom = frappe.db.count(
            "Item Price",
            filters={
                "price_list": selling_price_list,
                "item_code": item_code,
                "uom": item.stock_uom,
            },
        )

        if prices_with_uom > 0:
            filters["uom"] = item.stock_uom
        else:
            filters["uom"] = ["in", ["", None, item.stock_uom]]

        item_prices_data = frappe.get_all(
            "Item Price",
            fields=["item_code", "price_list_rate", "currency"],
            filters=filters,
        )

        item_price = 0
        if len(item_prices_data):
            item_price = item_prices_data[0].get("price_list_rate")
            currency = item_prices_data[0].get("currency")

        item.update(
            {
                "rate": item_price,
                "currency": currency,
                "item_code": item_code,
                "barcode": barcode,
                "actual_qty": 0,
                "item_barcode": search_item,
            }
        )
        return item


@frappe.whitelist()
def set_customer_info(fieldname, customer, value=""):
    field_with_doctype = {'mobile_no':'Customer','phone':'Address','phone_no_optional':'Address',
    'phone_no1optional':'Address','address_line1':'Address','address_line2':'Address','territory':"Customer",
    'customer_group':'Customer','city':'Address'}
    
    doctype = field_with_doctype[fieldname]
    if(doctype == 'Address'):
        address = frappe.get_all("Dynamic Link",{'link_doctype':"Customer", 'link_name':customer, 'parenttype':'Address'},pluck='parent')
        if(len(address)>=1):
            frappe.db.set_value('Address', address[0], fieldname, value)
            
            frappe.db.commit()

    if(doctype == 'Customer'):
        frappe.db.set_value('Customer', customer, fieldname, value)
        if(fieldname == 'mobile_no'):
            address = frappe.get_all("Dynamic Link",{'link_doctype':"Customer", 'link_name':customer, 'parenttype':'Address'},pluck='parent')
            if(len(address)>=1):
                frappe.db.set_value('Address', address[0], 'phone', value)
                frappe.db.commit()



    if fieldname == "loyalty_program":
        frappe.db.set_value("Customer", customer, "loyalty_program", value)

    contact = (
        frappe.get_cached_value("Customer", customer, "customer_primary_contact") or ""
    )

    if contact:
        contact_doc = frappe.get_doc("Contact", contact)
        if fieldname == "email_id":
            contact_doc.set("email_ids", [{"email_id": value, "is_primary": 1}])
            frappe.db.set_value("Customer", customer, "email_id", value)
        elif fieldname == "mobile_no":
            contact_doc.set("phone_nos", [{"phone": value, "is_primary_mobile_no": 1}])
            frappe.db.set_value("Customer", customer, "mobile_no", value)
        contact_doc.save()

    else:
        contact_doc = frappe.new_doc("Contact")
        contact_doc.first_name = customer
        contact_doc.is_primary_contact = 1
        contact_doc.is_billing_contact = 1
        if fieldname == "mobile_no":
            contact_doc.add_phone(value, is_primary_mobile_no=1, is_primary_phone=1)

        if fieldname == "email_id":
            contact_doc.add_email(value, is_primary=1)

        contact_doc.append("links", {"link_doctype": "Customer", "link_name": customer})

        contact_doc.flags.ignore_mandatory = True
        contact_doc.save()
        frappe.set_value(
            "Customer", customer, "customer_primary_contact", contact_doc.name
        )
    return customer

@frappe.whitelist()
def search_invoices_for_return(invoice_name, company):
    invoices_list = frappe.get_list(
        "Sales Invoice",
        filters={
            "name": ["like", f"%{invoice_name}%"],
            "company": company,
            "docstatus": 1,
            "is_return": 0,
        },
        fields=["name"],
        limit_page_length=0,
        order_by="customer",
    )
    data = []
    is_returned = frappe.get_all(
        "Sales Invoice",
        filters={"return_against": invoice_name, "docstatus": 1},
        fields=["name"],
        order_by="customer",
    )
    if len(is_returned):
        return data
    for invoice in invoices_list:
        data.append(frappe.get_doc("Sales Invoice", invoice["name"]))
    return data


def get_version():
    branch_name = get_app_branch("erpnext")
    if "12" in branch_name:
        return 12
    elif "13" in branch_name:
        return 13
    else:
        return 13


def get_app_branch(app):
    """Returns branch of an app"""
    import subprocess

    try:
        branch = subprocess.check_output(
            "cd ../apps/{0} && git rev-parse --abbrev-ref HEAD".format(app), shell=True
        )
        branch = branch.decode("utf-8")
        branch = branch.strip()
        return branch
    except Exception:
        return ""


@frappe.whitelist()
def get_offers(profile):
    pos_profile = frappe.get_doc("POS Profile", profile)
    company = pos_profile.company
    warehouse = pos_profile.warehouse
    date = nowdate()

    values = {
        "company": company,
        "pos_profile": profile,
        "warehouse": warehouse,
        "valid_from": date,
        "valid_upto": date,
    }
    data = frappe.db.sql(
        """
        SELECT *
        FROM `tabPOS Offer`
        WHERE 
        disable = 0 AND
        company = %(company)s AND
        (pos_profile is NULL OR pos_profile  = '' OR  pos_profile = %(pos_profile)s) AND
        (warehouse is NULL OR warehouse  = '' OR  warehouse = %(warehouse)s) AND
        (valid_from is NULL OR valid_from  = '' OR  valid_from <= %(valid_from)s) AND
        (valid_upto is NULL OR valid_from  = '' OR  valid_upto >= %(valid_upto)s)
    """,
        values=values,
        as_dict=1,
    )
    return data


@frappe.whitelist()
def get_customer_addresses(customer):
    return frappe.db.sql(
        """
        SELECT 
            address.name,
            address.address_line1,
            address.address_line2,
            address.address_title,
            address.city,
            address.state,
            address.country,
            address.address_type
        FROM `tabAddress` as address
        INNER JOIN `tabDynamic Link` AS link
				ON address.name = link.parent
        WHERE link.link_doctype = 'Customer'
            AND link.link_name = '{0}'
            AND address.disabled = 0
        ORDER BY address.name
        """.format(
            customer
        ),
        as_dict=1,
    )


@frappe.whitelist()
def make_address(args):
    args = json.loads(args)
    address = frappe.get_doc(
        {
            "doctype": "Address",
            "address_title": args.get("name"),
            "address_line1": args.get("address_line1"),
            "address_line2": args.get("address_line2"),
            "city": args.get("city"),
            "state": args.get("state"),
            "pincode": args.get("pincode"),
            "country": args.get("country"),
            "address_type": "Shipping",
            "links": [
                {"link_doctype": args.get("doctype"), "link_name": args.get("customer")}
            ],
        }
    ).insert()

    return address


def build_item_cache(item_code):
    parent_item_code = item_code

    attributes = [
        a.attribute
        for a in frappe.db.get_all(
            "Item Variant Attribute",
            {"parent": parent_item_code},
            ["attribute"],
            order_by="idx asc",
        )
    ]

    item_variants_data = frappe.db.get_all(
        "Item Variant Attribute",
        {"variant_of": parent_item_code},
        ["parent", "attribute", "attribute_value"],
        order_by="name",
        as_list=1,
    )

    disabled_items = set([i.name for i in frappe.db.get_all("Item", {"disabled": 1})])

    attribute_value_item_map = frappe._dict({})
    item_attribute_value_map = frappe._dict({})

    item_variants_data = [r for r in item_variants_data if r[0] not in disabled_items]
    for row in item_variants_data:
        item_code, attribute, attribute_value = row
        # (attr, value) => [item1, item2]
        attribute_value_item_map.setdefault((attribute, attribute_value), []).append(
            item_code
        )
        # item => {attr1: value1, attr2: value2}
        item_attribute_value_map.setdefault(item_code, {})[attribute] = attribute_value

    optional_attributes = set()
    for item_code, attr_dict in item_attribute_value_map.items():
        for attribute in attributes:
            if attribute not in attr_dict:
                optional_attributes.add(attribute)

    frappe.cache().hset(
        "attribute_value_item_map", parent_item_code, attribute_value_item_map
    )
    frappe.cache().hset(
        "item_attribute_value_map", parent_item_code, item_attribute_value_map
    )
    frappe.cache().hset("item_variants_data", parent_item_code, item_variants_data)
    frappe.cache().hset("optional_attributes", parent_item_code, optional_attributes)


def get_item_optional_attributes(item_code):
    val = frappe.cache().hget("optional_attributes", item_code)

    if not val:
        build_item_cache(item_code)

    return frappe.cache().hget("optional_attributes", item_code)


@frappe.whitelist()
def get_item_attributes(item_code):
    attributes = frappe.db.get_all(
        "Item Variant Attribute",
        fields=["attribute"],
        filters={"parenttype": "Item", "parent": item_code},
        order_by="idx asc",
    )

    optional_attributes = get_item_optional_attributes(item_code)

    for a in attributes:
        values = frappe.db.get_all(
            "Item Attribute Value",
            fields=["attribute_value", "abbr"],
            filters={"parenttype": "Item Attribute", "parent": a.attribute},
            order_by="idx asc",
        )
        a.values = values
        if a.attribute in optional_attributes:
            a.optional = True

    return attributes


@frappe.whitelist()
def create_payment_request(doc):
    doc = json.loads(doc)
    for pay in doc.get("payments"):
        if pay.get("type") == "Phone":
            if pay.get("amount") <= 0:
                frappe.throw(_("Payment amount cannot be less than or equal to 0"))

            if not doc.get("contact_mobile"):
                frappe.throw(_("Please enter the phone number first"))

            pay_req = get_existing_payment_request(doc, pay)
            if not pay_req:
                pay_req = get_new_payment_request(doc, pay)
                pay_req.submit()
            else:
                pay_req.request_phone_payment()

            return pay_req


def get_new_payment_request(doc, mop):
    payment_gateway_account = frappe.db.get_value(
        "Payment Gateway Account",
        {
            "payment_account": mop.get("account"),
        },
        ["name"],
    )

    args = {
        "dt": "Sales Invoice",
        "dn": doc.get("name"),
        "recipient_id": doc.get("contact_mobile"),
        "mode_of_payment": mop.get("mode_of_payment"),
        "payment_gateway_account": payment_gateway_account,
        "payment_request_type": "Inward",
        "party_type": "Customer",
        "party": doc.get("customer"),
        "return_doc": True,
    }
    return make_payment_request(**args)


def get_existing_payment_request(doc, pay):
    payment_gateway_account = frappe.db.get_value(
        "Payment Gateway Account",
        {
            "payment_account": pay.get("account"),
        },
        ["name"],
    )

    args = {
        "doctype": "Payment Request",
        "reference_doctype": "Sales Invoice",
        "reference_name": doc.get("name"),
        "payment_gateway_account": payment_gateway_account,
        "email_to": doc.get("contact_mobile"),
    }
    pr = frappe.db.exists(args)
    if pr:
        return frappe.get_doc("Payment Request", pr[0][0])


def make_payment_request(**args):
    """Make payment request"""

    args = frappe._dict(args)

    ref_doc = frappe.get_doc(args.dt, args.dn)
    gateway_account = get_gateway_details(args) or frappe._dict()

    grand_total = get_amount(ref_doc, gateway_account.get("payment_account"))
    if args.loyalty_points and args.dt == "Sales Order":
        from erpnext.accounts.doctype.loyalty_program.loyalty_program import (
            validate_loyalty_points,
        )

        loyalty_amount = validate_loyalty_points(ref_doc, int(args.loyalty_points))
        frappe.db.set_value(
            "Sales Order",
            args.dn,
            "loyalty_points",
            int(args.loyalty_points),
            update_modified=False,
        )
        frappe.db.set_value(
            "Sales Order",
            args.dn,
            "loyalty_amount",
            loyalty_amount,
            update_modified=False,
        )
        grand_total = grand_total - loyalty_amount

    bank_account = (
        get_party_bank_account(args.get("party_type"), args.get("party"))
        if args.get("party_type")
        else ""
    )

    existing_payment_request = None
    if args.order_type == "Shopping Cart":
        existing_payment_request = frappe.db.get_value(
            "Payment Request",
            {
                "reference_doctype": args.dt,
                "reference_name": args.dn,
                "docstatus": ("!=", 2),
            },
        )

    if existing_payment_request:
        frappe.db.set_value(
            "Payment Request",
            existing_payment_request,
            "grand_total",
            grand_total,
            update_modified=False,
        )
        pr = frappe.get_doc("Payment Request", existing_payment_request)
    else:
        if args.order_type != "Shopping Cart":
            existing_payment_request_amount = get_existing_payment_request_amount(
                args.dt, args.dn
            )

            if existing_payment_request_amount:
                grand_total -= existing_payment_request_amount

        pr = frappe.new_doc("Payment Request")
        pr.update(
            {
                "payment_gateway_account": gateway_account.get("name"),
                "payment_gateway": gateway_account.get("payment_gateway"),
                "payment_account": gateway_account.get("payment_account"),
                "payment_channel": gateway_account.get("payment_channel"),
                "payment_request_type": args.get("payment_request_type"),
                "currency": ref_doc.currency,
                "grand_total": grand_total,
                "mode_of_payment": args.mode_of_payment,
                "email_to": args.recipient_id or ref_doc.owner,
                "subject": _("Payment Request for {0}").format(args.dn),
                "message": gateway_account.get("message") or get_dummy_message(ref_doc),
                "reference_doctype": args.dt,
                "reference_name": args.dn,
                "party_type": args.get("party_type") or "Customer",
                "party": args.get("party") or ref_doc.get("customer"),
                "bank_account": bank_account,
            }
        )

        if args.order_type == "Shopping Cart" or args.mute_email:
            pr.flags.mute_email = True

        pr.insert(ignore_permissions=True)
        if args.submit_doc:
            pr.submit()

    if args.order_type == "Shopping Cart":
        frappe.db.commit()
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = pr.get_payment_url()

    if args.return_doc:
        return pr

    return pr.as_dict()


def get_amount(ref_doc, payment_account=None):
    """get amount based on doctype"""
    grand_total = 0
    for pay in ref_doc.payments:
        if pay.type == "Phone" and pay.account == payment_account:
            grand_total = pay.amount
            break

    if grand_total > 0:
        return grand_total

    else:
        frappe.throw(
            _("Payment Entry is already created or payment account is not matched")
        )


@frappe.whitelist()
def get_pos_coupon(coupon, customer, company):
    res = check_coupon_code(coupon, customer, company)
    return res


@frappe.whitelist()
def get_active_gift_coupons(customer, company):
    coupons = []
    coupons_data = frappe.get_all(
        "POS Coupon",
        filters={
            "company": company,
            "coupon_type": "Gift Card",
            "customer": customer,
            "used": 0,
        },
        fields=["coupon_code"],
    )
    if len(coupons_data):
        coupons = [i.coupon_code for i in coupons_data]
    return coupons


@frappe.whitelist()
def get_customer_info(customer):
    customer = frappe.get_doc("Customer", customer)
    link_addr_doc = frappe.get_all("Dynamic Link",filters={'link_doctype':'Customer','link_name':customer.name,'parenttype':'Address'}, pluck='parent')
    

    res = {"loyalty_points": None, "conversion_factor": None}
    if(len(link_addr_doc)):
        address = frappe.get_doc("Address",link_addr_doc[0])
        res["address_line1"] = address.address_line1
        res["address_line2"] = address.address_line2
        res["city"] = address.city

    
    res["mobile_no"] = customer.mobile_no
    res["customer_name"] = customer.customer_name 
    res["territory"] = customer.territory
    res["customer_group"] = customer.customer_group
    res['payment_terms'] = customer.payment_terms
    
    res["customer_price_list"] = customer.default_price_list
    res["posa_discount"] = customer.posa_discount
    res["name"] = customer.name
    res['is_credit_customer'] = customer.is_credit_customer
    res["loyalty_program"] = customer.loyalty_program
    res["customer_group_price_list"] = frappe.get_value(
        "Customer Group", customer.customer_group, "default_price_list"
    )

    if customer.loyalty_program:
        lp_details = get_loyalty_program_details_with_points(
            customer.name,
            customer.loyalty_program,
            silent=True,
            include_expired_entry=False,
        )
        res["loyalty_points"] = lp_details.get("loyalty_points")
        res["conversion_factor"] = lp_details.get("conversion_factor")
    print(res,'\n'*5)
    return res



def get_company_domain(company):
    return frappe.get_cached_value("Company", cstr(company), "domain")


# Customized By Thirvusoft
# Start
@frappe.whitelist()
def get_fields_for_denomination(pos_opening_shift):
    amounts = frappe.get_all("Denomination Rupees", pluck = 'amount',order_by = '`amount` desc')
    fields=[]
    for i in amounts:
        fields+=(
            {'fieldname':f'amt{i}','label':f"<b>Amount</b>",'default':i,'read_only':1,'fieldtype':'Currency',"hidden":1},
            {'fieldname':f'sales{i}','label':f"<b>Enter Count here (For ₹{i})</b>", 'fieldtype':"Currency"},
        )
    pos_opening_shift=frappe.get_doc("POS Opening Shift",pos_opening_shift)
    
    for i in pos_opening_shift.balance_details:
        if i.mode_of_payment != "Cash - Fruits & ice":
            fields+=(
                {'fieldname':f'amt{i.mode_of_payment}','label':f"<b>Mode of Payment</b>","hidden":1,'default':i.mode_of_payment,'read_only':1,'fieldtype':'Data'},
                {'fieldname':f'sales{i.mode_of_payment}','label':f"<b>Enter Amount here (For ₹{i.mode_of_payment})</b>", 'fieldtype':"Currency"},
            )

    return fields

@frappe.whitelist()
def batch_finder(ts_barcode=None,ts_item=None):
    if ts_barcode:
        ts_batchs=frappe.db.get_all('Batch', fields=['name','expiry_date','batch_qty','ts_selling_price'], filters={'barcode':ts_barcode, 'disabled':0})
        return(ts_batchs)
    else:
        ts_batchs=frappe.db.get_all('Batch', fields=['name'], filters={'item':ts_item})
        if ts_batchs:
            return(ts_batchs[len(ts_batchs)-1]["name"])
        else:
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
        if(ref_no == None):
            ref_no = "1234567"
        if(ref_date == None):
            ref_date = frappe.utils.datetime.datetime.now()
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

# End

@frappe.whitelist()
def update_feedback_status(customer,status):
    if(status == "false"):status=0
    else:status=1
    frappe.db.set_value("Customer", customer, 'feedback_required', status)