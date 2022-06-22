let filter;
let company;
frappe.ui.form.on('Delivery Trip',{
    refresh: function(frm,cdt,cdn){
        company = frm.doc.company;
        if(frm.doc.docstatus == 0){
        frm.add_custom_button( __("Sales Invoice"),function(){
            frappe.call({
                'method':"sks.sks.custom.py.delivery_trip.get_customer_territory",
                'args': {},
                callback(r){

                    var d = new frappe.ui.Dialog({
                        title: "Choose Invoices For Delivery 🛻🛻🛻🛻..",
                        fields: [
                            {label:'Customer',fieldname:'customer',fieldtype:'Link',options: 'Customer'},
                            {fieldtype:'Column Break'},
                            {label:'Invoice',fieldname:'invoice',fieldtype:'Link',options: 'Sales Invoice'},
                            {fieldtype:'Column Break'},
                            {label:'Outstanding greater than',fieldname:'outstanding',fieldtype:'Float'},
                            {label:'Detlivery date between',fieldname:'sec',fieldtype:'Section Break'},
                            {label:'From Date',fieldname:'from_date',fieldtype:'Date'},
                            {fieldtype:'Column Break'},
                            {label:'To Date',fieldname:'to_date',fieldtype:'Date'},
                            {label:'Select territory',fieldname:'sec1',fieldtype:'Section Break'},
                            {label:'Territory',fieldname:'territory',fieldtype: 'MultiSelectPills',
                            get_data: function() {
                                return r.message
                            }
                        }
                        ],
                        primary_action_label: "Submit",
                        primary_action: function(data){
                            filter = data
                            frappe.call({
                                method: "sks.sks.custom.py.delivery_trip.get_condition_from_dialog",
                                args: {
                                    data: data
                                },
                                callback(r){
<<<<<<< HEAD
                                        if(r.message.length == 0){
                                            frappe.throw({
                                                title: "No Invoice",
                                                message: "All Invoice are Deliver"
                                             })
                                        }
=======
>>>>>>> e7ed9646e8968c26748de06d44d007471731dd3e
                                    let p = locals[cdt][cdn]
                                    frm.set_value("delivery_stops",[])
                                        for(let i = 0; i<r.message.length;i++){
                                        cur_frm.add_child("delivery_stops")
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"customer",r.message[i]["customer"])
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"address",r.message[i]["customer_address"])
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"sales_invoice",r.message[i]["name"])
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"delivery_status",r.message[i]["delivery_status"])
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"reason",r.message[i]["reason"])
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"contact",r.message[i]["contact_person"])
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"time_of_delivery",r.message[i]["time_of_delivery"])
                                        frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"amount",r.message[i]["outstanding_amount"])
                                         }
                                        cur_frm.refresh_field('delivery_stops')


                                }
                            })
                            d.hide();
                            
                        }
                    })
                    d.show()
                }
            })
            
        }, __('Get customers from'))
    }
    },
    update_invoice: function(frm,cdt,cdn){
        for(let i=0;i<2;i++){
        if(frm.doc.sales_invoice){
            frappe.call({
                method: "sks.sks.custom.py.delivery_trip.update_invoice",
                args:{
                    invoice: frm.doc.sales_invoice,
                    fields:{
                        delivery_status: frm.doc.delivery_status,
                        reason:frm.doc.reason || "",
                        time_of_delivery: frm.doc.time_of_delivery 
                    },
                    callback(res){
                        cur_frm.refresh_field('delivery_stops')
                        frm.refresh()
                        let p = locals[cdt][cdn]
                                
                                frappe.call({
                                    method : "sks.sks.custom.py.delivery_trip.get_condition_from_dialog",
                                    args : {data: filter},
                                    callback(r){
                                        frm.set_value("delivery_stops",[])
                                            for(let i = 0; i<r.message.length;i++){
                                            cur_frm.add_child("delivery_stops")
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"customer",r.message[i]["customer"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"address",r.message[i]["customer_address"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"sales_invoice",r.message[i]["name"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"delivery_status",r.message[i]["delivery_status"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"reason",r.message[i]["reason"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"contact",r.message[i]["contact_person"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"time_of_delivery",r.message[i]["time_of_delivery"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"amount",r.message[i]["outstanding_amount"])
                                            cur_frm.refresh_field('delivery_stops')
                                            
                                        }
                                        cur_frm.refresh_field('delivery_stops')
                                        frm.refresh()
                                    }
                                })

                    }
                } 
            })
        }
    }
    //payment entry

    if(frm.doc.mode_of_payment && frm.doc.amount && frm.doc.sales_invoice && frm.doc.delivery_status == "Delivered"){
        frappe.call({
            method:"sks.sks.custom.py.delivery_trip.payment_entry",
            args:{
                mode: frm.doc.mode_of_payment,
                amount: frm.doc.amount,
                pending_invoice: frm.doc.sales_invoice,
                company: frm.doc.company,
            },
            callback(res){
                frappe.show_alert({
                    message: res.message[0],
                    indicator: res.message[1]
                });
                if(res.message[1] == 'red'){
                    frappe.throw({
                       title: "Amount Exceed",
                       message: "Paid Amount is greater than the Outstanding Amount. ("+res.message[2]+" > "+res.message[3]+")"
                    })
                }
            }
        })
    }
},
    sales_invoice: function(frm){
        let invoices=[];
        for(let i of frm.doc.delivery_stops){
            invoices.push(i.sales_invoice)
        }
        frm.set_query("sales_invoice", function(){
            return{
                filters: {
                    'name': ['in',invoices]
                }
            }
        })
    }

})

frappe.ui.form.on("Delivery Stop",{
    'detail': function(frm,cdt,cdn){
        let p = locals[cdt][cdn]
        if(p.sales_invoice){
        function update_fields(p,r) {
            let f = locals[p.parenttype][p.parent]
                        frm.set_value("delivery_stops",[])
                            for(let i = 0; i<r.message.length;i++){
                            cur_frm.add_child("delivery_stops")
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"customer",r.message[i]["customer"])
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"address",r.message[i]["customer_address"])
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"sales_invoice",r.message[i]["name"])
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"delivery_status",r.message[i]["delivery_status"])
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"reason",r.message[i]["reason"])
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"contact",r.message[i]["contact_person"])
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"time_of_delivery",r.message[i]["time_of_delivery"])
                            frappe.model.set_value(f.delivery_stops[i].doctype,f.delivery_stops[i].name,"amount",r.message[i]["outstanding_amount"])
                                }
                            cur_frm.refresh_field('delivery_stops')
        }

        let reason=p.reason
        if(reason == ""){reason = " "}
        let amount=p.amount
        if(amount == 0){amount = "0"}
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var d = new frappe.ui.Dialog({
            title: "Invoice: " + p.sales_invoice,
            fields: [
            {fieldname: 'sales_invoice',label: 'Invoice',fieldtype: 'Link', default:p.sales_invoice, read_only: 1,options:'Sales Invoice'},
            {fieldtype:'Column Break'},
            {fieldname: 'customer',label: 'Customer',fieldtype: 'Link', default:p.customer, read_only: 1,options:'Customer'},
            {fieldtype:'Column Break'},
            {fieldname: 'dis_amount',label: 'Amount',fieldtype: 'Currency', default:amount, read_only: 1},
            {fieldtype:'Section Break'},
            {fieldname: 'address',label: 'Address Name',fieldtype: 'Link', default:p.address, read_only: 1,options:'Address'},
            {fieldtype:'Column Break'},
            {fieldname: 'dis_reason',label: 'Reason',fieldtype: 'Data', default:reason, read_only: 1},
            {fieldtype:'Section Break',label: "Update Status"},
            {fieldname: 'delivery_status',label: 'Delivery Status',fieldtype: 'Select', options: ['Attempt','Delivered','Not Delivered','Ready To Dispatch', 'Reattempt,Returned'], default:p.delivery_status},
            {fieldtype:'Column Break'},
            {fieldname: 'reason',label: 'Reason',fieldtype: 'Data', default:reason},
            {fieldtype:'Section Break'},
            {fieldname: 'mode_of_payment',label: 'Mode of Payment',fieldtype: 'Link',options: 'Mode of Payment',default: 'Cash'},
            {fieldtype:'Column Break'},
            {fieldname: 'amount',label: 'Paid Amount',fieldtype: 'Currency'},
            {fieldtype:'Column Break'},
            {fieldname: 'time_of_delivery',label: 'Time of Delivery',fieldtype: 'Time', default:time},
            {fieldtype:'Section Break'},

        ],
        primary_action_label: "Update Invoice",
        primary_action: function(data){
             //payment entry

   if(data.mode_of_payment && data.amount && data.sales_invoice && data.delivery_status == "Delivered"){
    frappe.call({
        method:"sks.sks.custom.py.delivery_trip.payment_entry",
        args:{
            mode: data.mode_of_payment,
            amount: data.amount,
            pending_invoice: data.sales_invoice,
            company: company,
        },
        callback(res){
<<<<<<< HEAD
            // frappe.call({
            //     method: "sks.sks.custom.py.delivery_trip.get_condition_from_dialog",
            //     args: {
            //         data: filter
            //     },
            //     callback(r){
            //         update_fields(p,r)


            //     }
            // })
=======
            frappe.call({
                method: "sks.sks.custom.py.delivery_trip.get_condition_from_dialog",
                args: {
                    data: filter
                },
                callback(r){
                    update_fields(p,r)


                }
            })
>>>>>>> e7ed9646e8968c26748de06d44d007471731dd3e
            frappe.show_alert({
                message: res.message[0],
                indicator: res.message[1]
            });
            if(res.message[1] == 'red'){
                frappe.throw({
                   title: "Amount Exceed",
                   message: "Paid Amount is greater than the Outstanding Amount. ("+res.message[2]+" > "+res.message[3]+")"
                })
            }
        }
    })
}
            frappe.call({
                method: "sks.sks.custom.py.delivery_trip.update_invoice",
                args:{
                    invoice: p.sales_invoice,
                    fields: data
                },
                callback(res){
                frappe.call({
                    method: "sks.sks.custom.py.delivery_trip.get_condition_from_dialog",
                    args: {
                        data: filter
                    },
                    callback(r){
                        update_fields(p,r)


                    }
                })
                }
            })
  
            d.hide();
    }
        })
        d.show()
    }}
})