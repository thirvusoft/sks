
frappe.ui.form.on("Stock Verification",{
	select_bin:function(frm){
        var select_bin=frm.doc.select_bin
       
        console.log(select_bin)
        frappe.db.get_value('Bin', {name:frm.doc.select_bin}, ["actual_qty","item_code"] ,function(value) {
            frm.set_value('qty',value.actual_qty)
            console.log(value)
            frm.set_value("select_item",value.item_code)
    })

    }
})
frappe.ui.form.on("Stock Verification",{
	// stock:function(frm){
    //     let system_stock=frm.doc.stock
    //     let entry_stock=frm.doc.qty
    //     console.log(system_stock-entry_stock)
    
        
    // },
    verify:function(frm){
        let system_stock=frm.doc.stock
        let entry_stock=frm.doc.qty
        frm.set_value('difference',(system_stock-entry_stock))
    }
})