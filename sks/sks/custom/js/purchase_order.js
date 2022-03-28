frappe.ui.form.on("Purchase Order",{
	before_save:function(frm,cdt,cdn){
		var data=locals[cdt][cdn]
		var items_code=[]
		var items_rate=[]
		for(var i=0;i<data.items.length;i++){
			items_code.push(data.items[i].item_code)
			items_rate.push(data.items[i].rate)
		}
		frappe.call({
			method:"sks.sks.custom.py.purchase_order.last_purchase_price_validate",
			args:{items_code,items_rate},
			callback(r){
				frm.set_value("item_price_changed",r["message"])
			}
		})
	}
})