from warnings import filters
import frappe
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.item.item import get_item_defaults
from frappe.contacts.doctype.address.address import get_company_address
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils.data import cstr, flt
@frappe.whitelist()
def item_check_with_sales_order(item_code_checking=None,checking_sales_order=None,search_value=None):
    matched_item=0
    item_code_from_sales_order=frappe.get_doc("Sales Order",checking_sales_order)
    total_item=item_code_from_sales_order.__dict__["items"]
    len_items=len(total_item)
    item_batch_name=[]
    item_batch_mrp=[]
    if(item_code_checking != None):
        for j in range(0,len_items,1):
            if(item_code_checking == total_item[j].__dict__["item_code"]):
                item_code=total_item[j].__dict__["item_code"]
                matched_item=matched_item+1
                if search_value:
                    ts_item_barcode=frappe.get_all("Batch",{"item":item_code_checking,"disabled":0,"barcode":search_value},["name","ts_mrp"])
                    if ts_item_barcode:
                        if len(ts_item_barcode)==1:
                            item_batch_name.append(ts_item_barcode[0]["name"])
                            item_batch_mrp=[]
                        else:
                            for batch in ts_item_barcode:
                                item_batch_name.append(batch["name"])
                                item_batch_mrp.append(batch["ts_mrp"])
                break
    if(matched_item==1):
        matched_item=0
        return item_code,item_batch_name,item_batch_mrp
    else:
        return 0
    
from frappe import _
@frappe.whitelist()
def mandatory_validation(doc,event):
    ts_value=frappe.db.get_single_value("Thirvu Retail Settings","item_warehouse_fetching")
    if ts_value==1:
        item = doc.items
        items_with_no_warehouse=""
        for i in item:
            item_name =  frappe.get_doc("Item",i.item_code)
            if item_name.warehouse:
                for warehouse in item_name.warehouse:
                    if warehouse.company:
                        if warehouse.company == doc.company:
                            w_house = warehouse.storebin
                            if w_house:i.warehouse = w_house
            else:
                items_with_no_warehouse+="•"+item_name.item_code+'<br>'
        if items_with_no_warehouse:frappe.throw(_("Please Select warehouse for <br>{0}".format(items_with_no_warehouse)))
    
    ts_value=frappe.db.get_single_value("Thirvu Retail Settings","allow_only_if_delivery_note_items_match_with_sales_order_items")
    if ts_value==1:
        ts_item_barcodes=""
        for item in doc.items:
            if item.against_sales_order:
                if item.item_verified == 0:
                    ts_item_details=frappe.get_doc("Item",item.item_code)
                    if ts_item_details.barcodes:
                        ts_item_barcodes += "•"+item.item_code+'<br>'
        if ts_item_barcodes:
            frappe.throw(_("Below Items Are Not Verified, Please Check It... <br>{0}").format(ts_item_barcodes))
            
@frappe.whitelist()
def sales_order_to_delivery_note(day):
    so_doc=frappe.get_list("Sales Order",{"delivery_day":day,"status":"To Deliver and Bill"},pluck="name")
    if so_doc != []:
        delivery_today=0
        unsuccessful_converts=0
        for source_name in so_doc:
            so_doc=frappe.get_doc("Sales Order",source_name)
            if so_doc.is_against_delivery_note == 0:
                try:
                    skip_item_mapping=False
                    target_doc=None
                    def set_missing_values(source, target):
                        target.run_method("set_missing_values")
                        target.run_method("set_po_nos")
                        target.run_method("calculate_taxes_and_totals")
                        if source.company_address:
                            target.update({"company_address": source.company_address})
                        else:
                            # set company address
                            target.update(get_company_address(target.company))
                        if target.company_address:
                            target.update(get_fetch_values("Delivery Note", "company_address", target.company_address))
                    def update_item(source, target, source_parent):
                        target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.base_rate)
                        target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
                        target.qty = flt(source.qty) - flt(source.delivered_qty)
                        item = get_item_defaults(target.item_code, source_parent.company)
                        item_group = get_item_group_defaults(target.item_code, source_parent.company)
                        if item:
                            target.cost_center = (
                                frappe.db.get_value("Project", source_parent.project, "cost_center")
                                or item.get("buying_cost_center")
                                or item_group.get("buying_cost_center")
                            )
                    mapper = {
                        "Sales Order": {"doctype": "Delivery Note", "validation": {"docstatus": ["=", 1]}},
                        "Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
                        "Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
                    }
                    if not skip_item_mapping:
                        def condition(doc):
                            # make_mapped_doc sets js `args` into `frappe.flags.args`
                            if frappe.flags.args and frappe.flags.args.delivery_dates:
                                if cstr(doc.delivery_date) not in frappe.flags.args.delivery_dates:
                                    return False
                            return abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier != 1
                        mapper["Sales Order Item"] = {
                            "doctype": "Delivery Note Item",
                            "field_map": {
                                "rate": "rate",
                                "name": "so_detail",
                                "parent": "against_sales_order",
                            },
                            "postprocess": update_item,
                            "condition": condition,
                        }
                    target_doc = get_mapped_doc("Sales Order", source_name, mapper, target_doc, set_missing_values)
                    target_doc.set_onload("ignore_price_list", True)
                    target_doc.save()
                    frappe.db.commit()
                    delivery_today+=1
                except:
                    unsuccessful_converts+=1
            s_msg=f"No of delivery notes created :{delivery_today} \n"
            f_msg=f"No of failed orders to convert :{unsuccessful_converts}"
            if s_msg != "No of delivery notes created :0" and f_msg !="No of failed orders to convert :0":
                msg=s_msg+f_msg
            elif s_msg != "No of delivery notes created :":
                msg=s_msg
            elif f_msg !="No of failed orders to convert :":
                msg=f_msg
            return msg
    else:
        msg="No Sales Orders to convert"
        return msg
    
def validate_delivery_note(doc,event):
    for row in doc.items:
        if row.against_sales_order:
            so=frappe.get_doc("Sales Order",row.against_sales_order)
            so.is_against_delivery_note=1
            so.save()
            frappe.db.commit()
            break
            
