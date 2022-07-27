import frappe

def stock_entry(doc,action):
    s=[]
    if doc.stock_entry_type == "Repack":
        for i in doc.items:
            if i.s_warehouse:
                s.append(frappe.get_value("Batch",i.batch_no,"ts_valuation_rate"))
        for j in doc.items:
            if j.t_warehouse:
                j.valuation_rates = sum(s)/len(s)


def markup_and_markdown_calculator(document,event):
    if document.stock_entry_type == "Repack":
        ts_matched_item=[]
        ts_matched_selling_rate=[]
        for j in document.items:
            if j.t_warehouse:
                item = j.item_code
                v_rate = j.valuation_rates
                ts_item_detais=frappe.get_doc("Item",item)
                if ts_item_detais:
                    item_mrp = ts_item_detais.mrp
                    if(ts_item_detais.__dict__["select_selling_price_type"]=="Markdown"):
                        ts_markdown=(item_mrp/100)*ts_item_detais.__dict__["ts_markdown_price"]
                        ts_markdown=item_mrp-ts_markdown
                        if(ts_markdown<item_mrp and ts_markdown>v_rate):
                            ts_matched_item.append(item)
                            ts_matched_selling_rate.append(ts_markdown)
                            j.selling_rates = ts_matched_selling_rate[0]
                        else:
                            frappe.throw("In Markdown, the valuation rate is greater than the selling rate")
                            
                        # else:
                        #     ts_unmatched_item.append(item)
                        #     ts_unmatched_selling_rate.append(ts_markdown)
                        #     item_row = frappe._dict({})                                              
                        #     item_row.update({'items':item,'selling_rate':ts_markdown,'difference':round(abs(j.valuation_rate-ts_markdown),2)})
                        #     ts_markdown_items_to_verify.append(item_row)
                        #     ts_markdown_items += f"{ts_item_name}:{round(abs(item_mrp-ts_markdown),2)}\n"
                    
                    if(ts_item_detais.__dict__["select_selling_price_type"]=="Markup"):
                        ts_markup=(item_mrp/100)*ts_item_detais.__dict__["ts_markup_price"]
                        ts_markup=v_rate+ts_markup
                        if(ts_markup<item_mrp and ts_markup>v_rate):
                            ts_matched_item.append(item)
                            ts_matched_selling_rate.append(ts_markup)
                            j.selling_rates = ts_matched_selling_rate[0]    
                        else:
                            frappe.throw("In Markup, the selling rate is greater than the  valuation rate")
                
            #                 ts_unmatched_item.append(item)
            #                 ts_unmatched_selling_rate.append(ts_markup)
            #                 item_row = frappe._dict({})                                              
            #                 item_row.update({'items':item,'selling_rate':ts_markup,'difference':round(abs(item_mrp-ts_markup),2)})
            #                 ts_markup_items_to_verify.append(item_row)
            #                 ts_markup_items += f"{ts_item_name}:{round(abs(j.valuation_rate-ts_markup),2)}\n"
            # document.ts_markdown_items = ts_markdown_items
            # document.ts_markup_items = ts_markup_items
    
@frappe.whitelist()
def auto_batch_creations(expiry_date=None,item_rate=None,item_code=None,item_mrp=None,doctype_name=None,document_name=None):

    item_rate=eval(item_rate)
    item_code=eval(item_code)
    item_mrp=eval(item_mrp)

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
                    

    item_document=frappe.get_doc(doctype_name,document_name)
    if(item_changes_count==0):
        frappe.db.set_value("Item",item_code[i],"create_new_batch",0)
        for item in item_document.items:
            if(item_code[i]==item.__dict__["item_code"]):
                if(correct_batch_name!=0):
                    frappe.set_value(item.doctype,item.name,"batch_no",correct_batch_name)

    else:
        frappe.db.set_value("Item",item_code[i],"create_new_batch",1)
    
    item_changes_count=0
    item_changes_details=[]
    return 0