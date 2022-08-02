// frappe.ui.form.on("Purchase Invoice",{
// 	supplier:function(frm,cdt,cdn){
// 		var ts_data=locals[cdt][cdn]
// 		var ts_supplier=ts_data.supplier
//         if(ts_supplier!=""){
//             frappe.call({
//                 method:"sks.sks.custom.py.supplier_items_finder.ts_supplier_items_finder",
//                 args:{ts_supplier},
//                 callback(ts_r){
//                     var ts_supplier_matched_item=ts_r["message"]
//                     frm.set_query("item_code", "items", function() {
//                         return {
//                             query: "erpnext.controllers.queries.item_query",
//                             filters: {'item_code' : ["in", ts_supplier_matched_item],'is_purchase_item': 1}
//                         }
//                     })
//                 }
//             })
//         }
// 	}
// })

frappe.ui.form.on("Purchase Invoice Item",{
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