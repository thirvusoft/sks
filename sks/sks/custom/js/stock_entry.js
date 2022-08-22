var main_data
frappe.ui.form.on("Stock Entry",{
    stock_entry_type:function(frm,cdt,cdn){
        main_data=frm.doc
        console.log(main_data)
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