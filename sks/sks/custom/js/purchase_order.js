frappe.ui.form.on("Purchase Order",{
	supplier:function(frm,cdt,cdn){
		var main_data=locals[cdt][cdn]
		var ts_supplier=main_data.supplier
		if(ts_supplier!=""){
			// frappe.call({
			// 	method:"sks.sks.custom.py.supplier_items_finder.ts_supplier_items_finder",
			// 	args:{ts_supplier},
			// 	callback(ts_r){
			// 		var ts_supplier_matched_item=ts_r["message"]
			// 		frm.set_query("item_code", "items", function() {
			// 			return {
			// 				query: "erpnext.controllers.queries.item_query",
			// 				filters: {'item_code' : ["in", ts_supplier_matched_item],'is_purchase_item': 1}
			// 			}
			// 		})
			// 	}
			// }),
			frappe.db.get_single_value("Thirvu Retail Settings","add_item_from_not_processed_purchase_order").then(value =>{
				if(value==1){
					frappe.call({
						method:"sks.sks.custom.py.buying_module.not_processed_po",
						args:{ts_supplier},
						callback(ts_not_processed_po){
							if(ts_not_processed_po.message.length){
								const d = new frappe.ui.Dialog({
									size: "large",
									title:"Not Processed Purchase Orders",
									fields:[
									{fieldname:'thirvu_not_processed_po', fieldtype:'Table',cannot_add_rows: 1,in_place_edit: true, fields:[
									{
										label: 'Purchase Order',
										fieldname: 'purchase_order',
										fieldtype: 'Read Only',
										in_list_view:1,
										read_only:1,
										columns:2
									},
									],
									data:ts_not_processed_po.message},
									],
									primary_action_label: "Cancel and add items",
									primary_action : function(data){
										var purchase_order=[]
										var value = d.fields_dict.thirvu_not_processed_po.grid.get_selected_children()
										for (let i = 0; i<value.length;i++){
											if(value[i].__checked){
												purchase_order.push(value[i].purchase_order)
											}
										}
										if(purchase_order){
											frappe.call({
												method:"sks.sks.custom.py.buying_module.fetching_items_from_not_processed_po",
												args:{reqd_po:purchase_order},
												callback(po_items){
													cur_frm.set_value('items',[])
													for(let i = 0; i<po_items.message.length;i++){
														cur_frm.add_child("items")
														frappe.model.set_value(main_data.items[i].doctype,main_data.items[i].name,"item_code",po_items.message[i]['item_code'])
														frappe.model.set_value(main_data.items[i].doctype,main_data.items[i].name,"qty",po_items.message[i]['qty'])
													}
												}
											})
										}
										else{
											frappe.msgprint('NO Purchase Order is Selected')
										}
										d.hide()
									}
								})
								if(ts_not_processed_po.message){
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
		var data=locals[cdt][cdn]
		var ts_item_code=data.item_code
		if(ts_item_code!=""){
			frappe.call({
				method:"sks.sks.custom.py.item_mrp_finder.ts_mrp_finder",
				args:{ts_item_code},
				callback(ts_r){
					if(ts_r["message"]){ 
						frappe.model.set_value(cdt,cdn,"ts_mrp",ts_r["message"][0])
						frappe.model.set_value(cdt,cdn,"ts_selling_rate",ts_r["message"][1])
					}
				}
			}),
			frappe.db.get_single_value("Thirvu Retail Settings","purchased_and_sold_qty_alert").then(value =>{
				if(value==1){
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
					})
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