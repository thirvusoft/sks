var main_data
frappe.ui.form.on("Stock Entry",{
    stock_entry_type:function(frm,cdt,cdn){
        main_data=frm.doc
    },
    onload:function(frm,cdt,cdn){
        main_data=frm.doc
    },
    generate_label:function(frm,cdt,cdn){
        if (main_data.stock_entry_type=="Repack"){
            if (main_data.docstatus==1){
                frappe.call({
                    method:"sks.sks.custom.py.stock_entry.fetching_items",
                    args:{data:main_data.items},
                    callback(items){
                        var d = new frappe.ui.Dialog({
                            title: __('Select Item Code To Generate Label'),
                            fields:[
                                {fieldname:'items_to_generate_label', fieldtype:'Table',cannot_add_rows: 1,in_place_edit: true, fields:[
                                {
                                    label: 'Item Code',
                                    fieldname: 'item_code_label',
                                    fieldtype: 'Read Only',
                                    in_list_view:1,
                                    read_only:1,
                                    columns:2
                                },
                                {
                                    label: 'Batch',
                                    fieldname: 'batch',
                                    fieldtype: 'Read Only',
                                    in_list_view:1,
                                    read_only:1,
                                    columns:2
                                },
                                {
                                    label: 'Qty',
                                    fieldname: 'qty',
                                    fieldtype: 'Int',
                                    in_list_view:1,
                                    read_only:1,
                                    columns:2
                                },
                                ],
                                data:items.message},
                                ],
                                primary_action: function(data) {
                                    
                                    var final_list=[]
                                    var value = d.fields_dict.items_to_generate_label.grid.get_selected_children()
                                    for (let i = 0; i<value.length;i++){
                                        var item_code_labels=[]
                                        if(value[i].__checked){
                                            item_code_labels.push(value[i]["item_code_label"])
                                            item_code_labels.push(value[i]['qty'])
                                            if (value[i]['batch']){
                                                item_code_labels.push(value[i]['batch'])
                                            }
                                            else{
                                                item_code_labels.push("")
                                            }
                                            final_list.push(item_code_labels)
                                        }
                                    }
                                    if(item_code_labels){
                                        frappe.call({
                                            method:"sks.sks.custom.py.stock_entry.label_generation",
                                            args:{items:final_list},
                                        })
                                    }
                                    else{
                                        frappe.msgprint('No Items added are selected')
                                    }
                                    d.hide();
                                }
                        });d.show()
                    }
                })
            }
            else{
                frappe.throw({
                    title:("Message"),
                    message:('Submit the document to generate label')
                })
            }	
        }
    }
})
frappe.ui.form.on("Stock Entry Detail",{
    batch_no:function(frm,cdt,cdn){
        var data=locals[cdt][cdn]
        if (main_data.stock_entry_type =="Repack"){
            if (data.s_warehouse){
                if (data.batch_no){
                    frappe.call({
                        method:"sks.sks.custom.py.stock_entry.valuation_rate_fetching",
                        args:{batch_no:data.batch_no},
                        callback(valuation_rate){
                            frappe.model.set_value(cdt,cdn,"valuation_rates",valuation_rate.message)
                        }
                    })
                }
            }    
        }
    }
})
 