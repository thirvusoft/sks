frappe.ui.form.on('Delivery Trip',{
    territory : function(frm,cdt,cdn){
        let p = locals[cdt][cdn]
        if(p.territory){
            if(p.delivery_date){
                frappe.call({
                    method : "sks.sks.custom.py.delivery_trip.get_sales_invoice",
                    args : {territory : p.territory, date : p.delivery_date},
                    callback(r){
                        console.log(r.message)
                        frm.set_value("delivery_stops",[])
                            for(let i = 0; i<r.message.length;i++){
                            cur_frm.add_child("delivery_stops")
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"customer",r.message[i]["customer"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"address",r.message[i]["customer_address"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"sales_invoice",r.message[i]["name"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"delivery_status",r.message[i]["delivery_status"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"reason",r.message[i]["reason"])
                            console.log("aaaaaaaaaaaaaaaaaaa")
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
                        console.log(r.message)
                        frm.set_value("delivery_stops",[])
                            for(let i = 0; i<r.message.length;i++){
                            cur_frm.add_child("delivery_stops")
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"customer",r.message[i]["customer"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"address",r.message[i]["customer_address"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"sales_invoice",r.message[i]["name"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"delivery_status",r.message[i]["delivery_status"])
                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"reason",r.message[i]["reason"])
                            console.log("aaaaaaaaaaaaaaaaaaa")
                        }
                        cur_frm.refresh_field('delivery_stops')
                    }
                })
            }
        }
    },
    update_invoice: function(frm,cdt,cdn){
        if(frm.doc.sales_invoice){
            frappe.call({
                method: "sks.sks.custom.py.delivery_trip.update_invoice",
                args:{
                    invoice: frm.doc.sales_invoice,
                    fields:{
                        delivery_status: frm.doc.delivery_status,
                        reason:frm.doc.reason || ""
                    },
                    callback(res){
                        alert(frm.doc.reason)
                        console.log("Success")
                        let p = locals[cdt][cdn]
                        if(p.territory){
                            if(p.delivery_date){
                                for(let i=0;i<2;i++){
                                frappe.call({
                                    method : "sks.sks.custom.py.delivery_trip.get_sales_invoice",
                                    args : {territory : p.territory, date : p.delivery_date},
                                    callback(r){
                                        console.log(r.message)
                                        frm.set_value("delivery_stops",[])
                                            for(let i = 0; i<r.message.length;i++){
                                            cur_frm.add_child("delivery_stops")
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"customer",r.message[i]["customer"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"address",r.message[i]["customer_address"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"sales_invoice",r.message[i]["name"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"delivery_status",r.message[i]["delivery_status"])
                                            frappe.model.set_value(p.delivery_stops[i].doctype,p.delivery_stops[i].name,"reason",r.message[i]["reason"])
                                            cur_frm.refresh_field('delivery_stops')
                                            console.log("aaaaaaaaaaaaaaaaaaa")
                                        }
                                        cur_frm.refresh_field('delivery_stops')
                                        frm.refresh()
                                    }
                                })
                            }
                            }
                        }
                    }
                } 
            })
        }
    }
})