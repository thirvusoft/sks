frappe.ui.form.on("Purchase Invoice",{
	supplier:function(frm,cdt,cdn){
		var ts_data=locals[cdt][cdn]
		var ts_supplier=ts_data.supplier
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
})