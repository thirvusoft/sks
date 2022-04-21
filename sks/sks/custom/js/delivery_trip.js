frappe.ui.form.on('Delivery Trip',{
    territory : function(frm,cdt,cdn){
        let p = locals[cdt][cdn]
        if(p.territory){
            if(p.delivery_date){
                frappe.call({
                    method : "sks.sks.custom.py.delivery_trip.get_sales_invoice",
                    args : {territory : p.territory, date : p.delivery_date},
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
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"amount",r.message[i]["paid_amount"])
                        }
                        cur_frm.refresh_field('delivery_stops')
                    }
                })
            }
        }
    },
    delivery_date: function(frm,cdt,cdn){
        let p = locals[cdt][cdn]
        if(p.territory){
            if(p.delivery_date){
                frappe.call({
                    method : "sks.sks.custom.py.delivery_trip.get_sales_invoice",
                    args : {territory : p.territory, date : p.delivery_date},
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
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"amount",r.message[i]["paid_amount"])
                        }
                        cur_frm.refresh_field('delivery_stops')
                    }
                })
            }
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
                        time_of_delivery: frm.doc.time_of_delivery || None
                    },
                    callback(res){
                        cur_frm.refresh_field('delivery_stops')
                        frm.refresh()
                        let p = locals[cdt][cdn]
                        if(p.territory){
                            if(p.delivery_date){
                                
                                frappe.call({
                                    method : "sks.sks.custom.py.delivery_trip.get_sales_invoice",
                                    args : {territory : p.territory, date : p.delivery_date},
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
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"amount",r.message[i]["paid_amount"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"amount",r.message[i]["paid_amount"])
                                            cur_frm.refresh_field('delivery_stops')
                                            
                                        }
                                        cur_frm.refresh_field('delivery_stops')
                                        frm.refresh()
                                    }
                                })
                            
                            }
                        }
                    }
                } 
            })
        }
    }
    //payment entry

    if(frm.doc.mode_of_payment && frm.doc.amount && frm.doc.sales_invoice){
        frappe.call({
            method:"sks.sks.custom.py.delivery_trip.payment_entry",
            args:{
                mode: frm.doc.mode_of_payment,
                amount: frm.doc.amount,
                pending_invoice: frm.doc.sales_invoice,
                company: frm.doc.company,
            },
            callback(res){

            }
        })
    }
}
})