frappe.ui.form.on("Sales Order",{
    after_save:function(frm,cdt,cdn){
        frappe.db.get_single_value("SKS Settings","customer_transaction_history").then(value =>{
            if(value==1){
                var data=locals[cdt][cdn]
                if(cur_frm.doc.docstatus!=1){
                    frappe.call({
                        method:"sks.sks.custom.py.sales_order.customer_transaction_history",
                        args:{
                            customer:data.customer
                        },
                        callback: function(r){
                            const d = new frappe.ui.Dialog({
                                title: "Customer transaction history",
                                static: true,
                                fields:[
                                {
                                    fieldname:'table',
                                    fieldtype:'HTML',
                                    label:'Table'
                                },
                                {
                                    fieldname:'items_add',
                                    fieldtype:'MultiSelectPills',
                                    label:'Select items to be added',
                                    get_data: function() {
                                        return r.message[2]
                                    }
                                }
                                ],
                                primary_action : function(data){
                                    frappe.call({
                                        method:"sks.sks.custom.py.sales_order.item_append",
                                        args:{item_code:data.items_add,current_document:cur_frm.doc.name},
                                    callback(r){
                                        frm.reload_doc();
                                    }
                                    })
                                    d.hide()
                                }
                            })
                        var template = "<table><tbody>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td> {{ rows[row][col] }}</td> <td> {{ days[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table>"
                        d.set_df_property('table', 'options', frappe.render(template, {rows:r.message[0], days:r.message[1]}));
                        if(r.message[0].length){
                            d.show();
                        }
                        }
                    })
                }
            }
        })    
    }
 })
 

frappe.ui.form.on("Sales Order",{
    set_warehouse:function(frm,cdt,cdn){
        var data=locals[cdt][cdn]
        frappe.call({
            method:"sks.sks.custom.py.sales_order.subwarehouse",
            args:{sub_warehouse:data.set_warehouse,company:data.company},
            callback(r){
                if(frm.fields_dict["items"].grid.get_field('item_code')) {
                    frm.set_query("item_code", "items", function() {
                        return {
                            query: "erpnext.controllers.queries.item_query",
                            filters: {'item_code' : ["in", r["message"]],'is_sales_item': 1, 'customer': cur_frm.doc.customer}
                        }
                    })
                }
            }
        })
    }
})


var parent_data
frappe.ui.form.on("Sales Order",{
    onload:function(frm,cdt,cdn){
        parent_data=locals[cdt][cdn]
    }
})
frappe.ui.form.on("Sales Order Item",{
    qty:function(frm,cdt,cdn){
        frappe.db.get_single_value("SKS Settings","reserved_stock").then(value =>{
            if(value==0){
                var data = locals[cdt][cdn]
                var item_code=data.item_code
                var item_qty=data.qty
                var source_warehouse=data.warehouse
                frappe.call({
                    method:"erpnext.stock.dashboard.item_dashboard.get_data",
                    args:{item_code,warehouse:source_warehouse},
                    callback(r){
                        var projected_qty=r.message[0].projected_qty     
                        if(item_qty>projected_qty){
                            for(var i=0;i<parent_data.items.length;i++){
                                if(item_code==parent_data.items[i].item_code){
                                    frappe.model.set_value(parent_data.items[i].doctype,parent_data.items[i].name,"qty",0)
                                    frappe.throw({
                                        title:"Stock Unavailable",
                                        message:"For Item : "+item_code+", The Quantity must be less than : "+projected_qty
                                    })
                                }
                            }
                        }
                    }
                })
            }
        })
    }
})