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
    onload:function(frm,cdt,cdn){
        frm.set_query("set_warehouse", function() {
            return {
                filters: [
                    ["Warehouse", "company", "in", ["", cstr(frm.doc.company)]],
				    ["Warehouse", "is_group", "=",1]
                ]
            };
        });
    },
    set_warehouse:function(frm,cdt,cdn){
        var data=locals[cdt][cdn]
        frappe.call({
            method:"sks.sks.custom.py.sales_order.subwarehouse",
            args:{sub_warehouse:data.set_warehouse,company:data.company},
            callback(r){
                    var subwarehouse_item_code=r["message"][0]
                    frm.set_query("item_code", "items", function() {
                        return {
                            query: "erpnext.controllers.queries.item_query",
                            filters: {'item_code' : ["in", subwarehouse_item_code],'is_sales_item': 1, 'customer': cur_frm.doc.customer}
                        }
                    })
            }
        })
    },
    before_submit:function(frm,cdt,cdn){
        if(frm.doc.status=="Draft"){
            var data=locals[cdt][cdn]
            var doctype_name=data.doctype
            var document_name=data.name
            var total_item_code=[]
            for(var i=0;i<data.items.length;i++){
                total_item_code.push(data.items[i].item_code)
            }
            frappe.call({
                method:"sks.sks.custom.py.sales_order.subwarehouse",
                args:{sub_warehouse:data.set_warehouse,company:data.company},
                callback(r){
                        var subwarehouse_item_codes=r["message"][0]
                        var subwarehouse_item_bins=r["message"][1]
                        frappe.call({
                            method:"sks.sks.custom.py.sales_order.bins",
                            args:{total_item_code,subwarehouse_item_codes,subwarehouse_item_bins,doctype_name,document_name},
                            callback(r){
                                if(r["message"]==0){
                                    frm.refresh();
                                }
                            }
                        })
                }
            })
        }
    }
})

var loop
frappe.ui.form.on("Sales Order",{
    onload:function(){
        loop=0
    }
})
frappe.ui.form.on("Sales Order",{
	after_save:function(frm,cdt,cdn){
        frappe.db.get_single_value("SKS Settings","credit_bill_history").then(value =>{
            if(value==1){
                if(cur_frm.doc.docstatus!=1){
                    if(loop==0){
                        var data1 = locals[cdt][cdn]
                        var customer = data1.customer
                        frappe.call({
                            method:"sks.sks.custom.py.sales_order.customer_credit_sale",
                            args:{customer},
                            callback : function(r){
                                if(r.message[2]>0){
                                    var d = new frappe.ui.Dialog({
                                        size: "extra large",
                                        title:"Customer: "+ customer +"'s Outstanding Amount",
                                        fields:[
                                            {'fieldname':'alert','fieldtype':'HTML','read_only':1,'bold':1},
                                            {'label':'Outstanding Amount','fieldname':'outstanding','fieldtype':'Currency','default':r.message[2],'read_only':1},
                                        ],
                                        primary_action : function(data){
                                            loop=loop+1
                                            frm.set_value("outstanding_amount",data.outstanding)
                                            var data1 = locals[cdt][cdn]
                                            var over_all_total = data1.outstanding_amount+data1.total
                                            cur_frm.set_value("outstanding_amount_and_total_amount",over_all_total)
                                            d.hide();

                                        }
                                    })
                                    var template=r.message[3]
                                    d.set_df_property("alert","options",frappe.render(template,{}))
                                    d.show();
                                }
                            }  
                        })
                    }
                }
                if(loop==0){
                    loop=loop+1
                    var data1 = locals[cdt][cdn]
                    var over_all_total = data1.outstanding_amount+data1.total
                    cur_frm.set_value("outstanding_amount_and_total_amount",over_all_total)
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
            if(value==1){
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
                                        message:"For Item : "+item_code+", Available Quantity : "+projected_qty
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
 