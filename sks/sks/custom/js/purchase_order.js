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
			}),
			frappe.db.get_single_value("Thirvu Retail Settings","add_item_from_not_processed_purchase_order").then(value =>{
				if(value==1){
					frappe.call({
						method:"sks.sks.custom.py.buying_module.not_processed_po",
						args:{ts_supplier},
						callback(ts_po_details){
							if(ts_po_details){
								const d = new frappe.ui.Dialog({
									title: "Pending purchase orders with the supplier",
									static: true,
									fields:[
									{
										fieldname:'table',
										fieldtype:'HTML',
										label:'Table'
									},
									{
										fieldname:'po_add',
										fieldtype:'MultiSelectPills',
										label:'Select items to be added',
										get_data: function() {
											return ts_po_details.message[1]
										}
									}
									],
									primary_action_label: "Cancel and add items",
									primary_action : function(data){
										frappe.call({
											method:"sks.sks.custom.py.buying_module.fetching_items_from_not_processed_po",
											args:{reqd_po:data.po_add},
											callback(po_items){
												for(let i = 0; i<po_items.message.length;i++){
													frappe.model.set_value(ts_data.items[i].doctype,ts_data.items[i].name,"item_code",po_items.message[i][0])
													frappe.model.set_value(ts_data.items[i].doctype,ts_data.items[i].name,"qty",po_items.message[i][1])
													if(i<(po_items.message.length-1)){
														cur_frm.add_child("items")
													}
												}
											}
										})
										d.hide()
									}
								})
								if(ts_po_details.message[0]){
									var template = ts_po_details.message[0]
									d.set_df_property('table', 'options', frappe.render(template,{}))
									d.show();
								}
								
							}
			
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
			}),
			frappe.call({

				method:"sks.sks.custom.py.buying_module.last_purchased_and_sold_qty",
				args:{ts_item_code},
				callback(returned){
					if(returned.message[0] > 0 && returned.message[1] > 0){
						frappe.show_alert({ message: __("Last purchased Qty : "+returned.message[0] +"  Total Sold Qty : "+returned.message[1]), indicator: 'red' });
					}
					else if(returned.message[0] > 0){
						frappe.show_alert({ message: __("Last purchased Qty : "+returned.message[0] +"  Total Sold Qty : 0"), indicator: 'red' });

					}
					else if(returned.message[1] > 0){
						frappe.show_alert({ message: __("Last purchased Qty : 0" +"  Total Sold Qty : "+returned.message[1]), indicator: 'red' });

					}
				}
			}),
			frappe.db.get_single_value("Thirvu Retail Settings","buying_rate_calculation").then(value =>{
				if(value==1){
					frappe.call({
						method:"sks.sks.custom.py.buying_module.buying_rate_finder",
						args:{ts_item_code},
						callback(buying_return){
							if(buying_return.message){
								frappe.model.set_value(cdt,cdn,"rate",buying_return.message)
							}
						}
					})
				}
			})
		}
	}
})
