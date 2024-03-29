# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

# import frappe
import frappe
import json
from frappe import _
from frappe.utils import flt, getdate
from frappe.model.document import Document

class RequiredQuantityPrediction(Document):
	pass

@frappe.whitelist()
def required_quantity_prediction(data):
	data = json.loads(data)
	print(data["required_days"])
	items=[]
	item = {}
	item["name"] = data["item"]
	item["safety_stock"] = data["safety_stock"]
	item["lead_time_days"] = data["lead_time_days"]
	items.append(item)
	filters={}
	filters["from_date"]=data["from_date"]
	filters["to_date"]=data["to_date"]

	if not filters:
		filters = {}
	float_precision = frappe.db.get_default("float_precision")

	condition = get_condition(filters)

	avg_daily_outgoing = 0
	diff = ((getdate(filters.get("to_date")) - getdate(filters.get("from_date"))).days) + 1
	if diff <= 0:
		frappe.throw(_("'From Date' must be after 'To Date'"))

	consumed_item_map = get_consumed_items(condition)
	delivered_item_map = get_delivered_items(condition)

	for item in items:
		total_outgoing = flt(consumed_item_map.get(item["name"], 0)) + flt(
			delivered_item_map.get(item["name"], 0)
		)
		avg_daily_outgoing = flt(total_outgoing / diff, float_precision)
	needed_qty = avg_daily_outgoing * data["required_days"]
	return needed_qty


def get_consumed_items(condition):
	purpose_to_exclude = [
		"Material Transfer for Manufacture",
		"Material Transfer",
		"Send to Subcontractor",
	]

	condition += """
		and (
			purpose is NULL
			or purpose not in ({})
		)
	""".format(
		", ".join(f"'{p}'" for p in purpose_to_exclude)
	)
	condition = condition.replace("posting_date", "sle.posting_date")

	consumed_items = frappe.db.sql(
		"""
		select item_code, abs(sum(actual_qty)) as consumed_qty
		from `tabStock Ledger Entry` as sle left join `tabStock Entry` as se
			on sle.voucher_no = se.name
		where
			actual_qty < 0
			and is_cancelled = 0
			and voucher_type not in ('Delivery Note', 'Sales Invoice')
			%s
		group by item_code"""
		% condition,
		as_dict=1,
	)

	consumed_items_map = {item.item_code: item.consumed_qty for item in consumed_items}
	return consumed_items_map


def get_delivered_items(condition):
	dn_items = frappe.db.sql(
		"""select dn_item.item_code, sum(dn_item.stock_qty) as dn_qty
		from `tabDelivery Note` dn, `tabDelivery Note Item` dn_item
		where dn.name = dn_item.parent and dn.docstatus = 1 %s
		group by dn_item.item_code"""
		% (condition),
		as_dict=1,
	)

	si_items = frappe.db.sql(
		"""select si_item.item_code, sum(si_item.stock_qty) as si_qty
		from `tabSales Invoice` si, `tabSales Invoice Item` si_item
		where si.name = si_item.parent and si.docstatus = 1 and
		si.update_stock = 1 %s
		group by si_item.item_code"""
		% (condition),
		as_dict=1,
	)

	dn_item_map = {}
	for item in dn_items:
		dn_item_map.setdefault(item.item_code, item.dn_qty)

	for item in si_items:
		dn_item_map.setdefault(item.item_code, item.si_qty)

	return dn_item_map


def get_condition(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and posting_date between '%s' and '%s'" % (
			filters["from_date"],
			filters["to_date"],
		)
	else:
		frappe.throw(_("From and To dates required"))
	return conditions