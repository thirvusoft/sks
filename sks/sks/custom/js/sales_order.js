var data,loop,warehouse,company,loading,parent_data
frappe.ui.form.on("Sales Order",{
    onload:function(frm,cdt,cdn){
        loading=0
        loop=0
        parent_data=locals[cdt][cdn]
    },
    company:function(frm,cdt,cdn){
        company=cur_frm.doc.company
    },
    after_save:function(frm,cdt,cdn){
        if(loading==0){
            frappe.db.get_single_value("Thirvu Retail Settings","customer_transaction_history").then(value =>{
                if(value==1){
                    var data=locals[cdt][cdn]
                    var item_codes=[]
                    for(var i=0;i<data.items.length;i++){
                        item_codes.push(data.items[i].item_code)
                    }
                    if(cur_frm.doc.docstatus!=1){
                        frappe.call({
                            method:"sks.sks.custom.py.sales_order.customer_transaction_history",
                            args:{
                                customer:data.customer,item_codes
                            },
                            callback: function(r){
                                if(r.message[4]!=0){
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
                                                return r.message[5]
                                            }
                                        }
                                        ],
                                        primary_action : function(data){
                                            frappe.call({
                                                method:"sks.sks.custom.py.sales_order.item_append",
                                                args:{item_code:data.items_add,current_document:cur_frm.doc.name},
                                                callback(r){
                                                    frm.reload_doc();
                                                    setTimeout(() => {
                                                        loading=loading+1;
                                                    }, 1500);
                                                }
                                            })
                                            d.hide()
                                        }
                                    })
                                    if(r.message[1]){
                                        var template = r.message[3]
                                        d.set_df_property('table', 'options', frappe.render(template,{}))
                                        d.show();
                                    }
                                }
                            }
                        })
                    }
                }
                loading=loading+1
            })
        }
    },
    customer:function(frm,cdt,cdn){
        frappe.db.get_single_value("Thirvu Retail Settings","credit_bill_history").then(value =>{
            if(value==1){
                if(cur_frm.doc.docstatus!=1){
                    // if(loop==0){
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
                    // }
                }
                if(loop==0){
                    loop=loop+1
                    var data1 = locals[cdt][cdn]
                    var over_all_total = data1.outstanding_amount+data1.total
                    cur_frm.set_value("outstanding_amount_and_total_amount",over_all_total)
                }
            }
        })
    },
    delivery_date:function(frm,cdt,cdn){
		var day = new Date(cur_frm.doc.delivery_date);
		var weekdays=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
		cur_frm.set_value("delivery_day",weekdays[day.getDay()])
	}
})
frappe.ui.form.on("Sales Order Item",{
    qty:function(frm,cdt,cdn){
        frappe.db.get_single_value("Thirvu Retail Settings","reserved_stock").then(value =>{
            if(value==1){
                var data = locals[cdt][cdn]
                var item_code=data.item_code
                var item_qty=data.qty
                for(var i=0;i<subwarehouse_item_codes.length;i++){
                    if(subwarehouse_item_codes[i]==item_code){
                        var source_warehouse=subwarehouse_item_bins[i]
                        item_code=subwarehouse_item_codes[i]
                    }
                }
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
    },
    item_code:function(frm,cdt,cdn){
            data=locals[cdt][cdn]
            var item_code=data.item_code
            var actual_qty =0
            actual_qty = data.actual_qty
            if(item_code){
                frappe.show_alert({ message: __('Stock Quantity for '+actual_qty), indicator: 'green' });
            }  
        },
       
    }
)

