frappe.ui.form.on('Delivery Trip',{
    territory : function(frm,cdt,cdn){
        let p = locals[cdt][cdn]
        if(p.territory){
            frappe.call({
                method : "sks.sks.custom.py.delivery_trip.get_sales_invoice",
                args : {territory : p.territory},
                callback(r){
                    console.log(r.message)
                    frappe.model.set_value(cdt,cdn,"delivery_stops",[])
                    frappe.model.set_value(cdt,cdn,"delivery_stops",r.message)
                }
            })
        }
    }
})