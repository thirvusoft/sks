
frappe.ui.form.on("Stock Verification",{
	select_bin:function(frm){
        var select_bin=frm.doc.select_bin
        frappe.db.get_value('Bin', {name:frm.doc.select_bin}, ["actual_qty","item_code","warehouse"] ,function(value) {
            frm.set_value('qty',value.actual_qty)
            frm.set_value("select_item",value.item_code)
			frm.set_value("item_warehouse",value.warehouse)
    })

    }
})
frappe.ui.form.on("Stock Verification",{
    verify:function(frm){
        let system_stock=frm.doc.stock
        let entry_stock=frm.doc.qty
        frm.set_value('difference',(system_stock-entry_stock))
    },
    setup: function (frm) {
		frm.set_query("batch_no", function () {
			return {
               
				filters: { 'item': frm.doc.select_item ,'disabled':0,'expiry_date':[">" ,Date.now]}
			};
        }
)}
    
})