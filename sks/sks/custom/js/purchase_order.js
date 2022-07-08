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

frappe.ui.form.on("Purchase Order",{
	supplier:function(frm,cdt,cdn){
		var ts_data=locals[cdt][cdn]
		var ts_supplier=ts_data.supplier
		if(ts_supplier!=""){
			frappe.call({
				method:"sks.sks.custom.py.supplier_items_finder.ts_supplier_items_finder",
				args:{ts_supplier},
				callback(ts_r){
					var ts_supplier_matched_item=ts_r["message"]
					frm.set_query("item_code", "items", function() {
						return {
							query: "erpnext.controllers.queries.item_query",
							filters: {'item_code' : ["in", ts_supplier_matched_item],'is_purchase_item': 1}
						}
					})
				}
			})
		}
	}
})
frappe.ui.form.on("Purchase Order Item",{
	item_code:function(frm,cdt,cdn){
		var ts_data=locals[cdt][cdn]
		var ts_item_code=ts_data.item_code
		if(ts_item_code!=""){
			frappe.call({
				method:"sks.sks.custom.py.item_mrp_finder.ts_mrp_finder",
				args:{ts_item_code},
				callback(ts_r){
					frappe.model.set_value(cdt,cdn,"ts_mrp",ts_r.message)
				}
			})
		}
	}
})