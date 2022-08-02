import frappe
from frappe import _
def stock_entry(doc,action):
    item_wise_batch_details=[]
    if doc.stock_entry_type == "Repack":
        for item_source_warehouse in doc.items:
            if item_source_warehouse.s_warehouse:
                item_wise_batch_details.append(frappe.get_value("Batch",item_source_warehouse.batch_no,"ts_valuation_rate"))
                item_source_warehouse.basic_rate = item_source_warehouse.valuation_rates
        for item_target_warehouse in doc.items:
            if item_target_warehouse.t_warehouse:
                item_target_warehouse.valuation_rates = sum(item_wise_batch_details)
        markup_and_markdown_calculator(doc)

def markup_and_markdown_calculator(document):
    if document.stock_entry_type == "Repack":
        ts_matched_item=[]
        ts_matched_selling_rate=[]
        for item in document.items:
            if item.t_warehouse:
                item_code = item.item_code
                v_rate = item.valuation_rates
                ts_item_detais=frappe.get_doc("Item",item_code)
                if ts_item_detais:
                    item_mrp = ts_item_detais.mrp
                    if(ts_item_detais.__dict__["select_selling_price_type"]=="Markdown"):
                        ts_markdown=(item_mrp/100)*ts_item_detais.__dict__["ts_markdown_price"]
                        ts_markdown=item_mrp-ts_markdown
                        if(ts_markdown<item_mrp and ts_markdown>v_rate):
                            ts_matched_item.append(item_code)
                            ts_matched_selling_rate.append(ts_markdown)
                            item.selling_rates = ts_matched_selling_rate[0]
                        else:
                            frappe.throw(_("In Markdown, The selling rate is lesser then the valuation rate for the below item please contact higher authority people <br>•{0}").format(ts_item_detais.name))
                    
                    
                    if(ts_item_detais.__dict__["select_selling_price_type"]=="Markup"):
                        ts_markup=(item_mrp/100)*ts_item_detais.__dict__["ts_markup_price"]
                        ts_markup=v_rate+ts_markup
                        if(ts_markup<item_mrp and ts_markup>v_rate):
                            ts_matched_item.append(item_code)
                            ts_matched_selling_rate.append(ts_markup)
                            item.selling_rates = ts_matched_selling_rate[0]    
                        else:
                            frappe.throw(_("In Markup, The selling rate is greater then the MRP for the below item please contact higher authority people <br>•{0}").format(ts_item_detais.name))
    
@frappe.whitelist()
def auto_batch_creations(doc,event):
    access=frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation")
    if access==1:
        item_rate=[]
        item_code=[]
        item_mrp=[]
        # expiry_date=[]
        for item in doc.items:
            if item.t_warehouse:
                item_rate.append(item.valuation_rates)
                item_code.append(item.item_code)
                item_mrp.append(item.mrp_rates)
                # expiry_date.append(item.expire_dates)

        matched_batch_name=[]
        matched_creation_date=[]
        item_changes_count=0
        item_changes_details=[]
        correct_batch_name=0
        batch_expiry=frappe.get_all("Batch",fields=["name","ts_valuation_rate","item","expiry_date","creation","ts_mrp"])
        for i in range(0,len(item_code),1):
            for j in range(0,(len(batch_expiry)),1):
                if(item_code[i]==batch_expiry[j]["item"]):
                    matched_batch_name.append(batch_expiry[j]["name"])
            for l in range(0,len(matched_batch_name),1):
                for n in range(0,(len(batch_expiry)),1):
                    if(matched_batch_name[l]==batch_expiry[n]["name"]):
                        matched_creation_date.append(batch_expiry[n]["creation"])
            for c in range(0,(len(batch_expiry)),1):
                if(matched_creation_date!=[]):
                    if(max(matched_creation_date)==batch_expiry[c]["creation"]):
                        correct_batch_name=batch_expiry[c]["name"]
                        # formatted_expiry_date=getdate(expiry_date[i])
                        # if(batch_expiry[c]["expiry_date"]!=formatted_expiry_date):
                        #     item_changes_count=item_changes_count+1
                        #     item_changes_details.append("Expiry date")
                        if(batch_expiry[c]["ts_mrp"]!=item_mrp[i]):
                            item_changes_count=item_changes_count+1
                            item_changes_details.append("MRP")
                        if(batch_expiry[c]["ts_valuation_rate"]!=item_rate[i]):
                            item_changes_count=item_changes_count+1
                            item_changes_details.append("Valuation Rate")
                        
        if(item_changes_count==0):
            frappe.db.set_value("Item",item_code[i],"create_new_batch",0)
            for item in doc.items:
                if(item_code[i]==item.__dict__["item_code"]):
                    if(correct_batch_name!=0):
                        print(correct_batch_name)
                        item.batch_no=correct_batch_name

        else:
            frappe.db.set_value("Item",item_code[i],"create_new_batch",1)
        
        item_changes_count=0
        item_changes_details=[]