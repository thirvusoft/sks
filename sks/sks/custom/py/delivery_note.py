from warnings import filters
import frappe
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.item.item import get_item_defaults
from frappe.contacts.doctype.address.address import get_company_address
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils.data import cstr, flt
import json
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
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
def sales_order_to_delivery_note(data):
    data=json.loads(data)
    if data["mode_of_delivery"] == "Is Local Delivery":
        so_doc=frappe.get_list("Sales Order",{"is_against_delivery_note":0,"is_local_delivery":1,"status":("in",("To Deliver","To Deliver and Bill"))},pluck="name")
    else:
        so_doc=frappe.get_list("Sales Order",{"is_against_delivery_note":0,"mode_of_delivery":data["mode_of_delivery"],"delivery_day":data["delivery_day"],"status":("in",("To Deliver","To Deliver and Bill"))},pluck="name")
    if so_doc != []:
        convereted_doc_count=0
        not_converted_doc=""
        for source_name in so_doc:
            try:
                delivery_note_doc=(make_delivery_note(source_name))
                delivery_note_doc.save()
                dn_new_doc=frappe.get_doc("Sales Order",source_name)
                dn_new_doc.is_against_sales_invoice = 1
                dn_new_doc.save()
                frappe.db.commit()
                convereted_doc_count+=1
            except:
                not_converted_doc += "•"+source_name+'<br>'
            s_msg=f"No Of Delivery Notes Created : {convereted_doc_count} <br>"
            f_msg=f"Below Sales Order Are Not Converted To Deliver Note :<br> {not_converted_doc}"
            if s_msg != "No Of Delivery Notes Created :0" and not_converted_doc != "":
                msg=s_msg+f_msg
            elif s_msg != "No Of Delivery Notes Created :":
                msg=s_msg
            elif f_msg !="Below Sales Order Are Not Converted To Deliver Note :":
                msg=f_msg
        return msg
    else:
        msg="No Sales Orders To Convert"
        return msg

