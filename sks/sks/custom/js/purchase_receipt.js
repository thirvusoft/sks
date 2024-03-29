var total_barcode_number_item=[]
var total_barcode_item_code=[]
var item_codes=[]
var data
frappe.ui.form.on("Purchase Receipt",{
	onload:function(frm,cdt,cdn){
		frappe.db.get_single_value("Thirvu Retail Settings","item_verifed_in_purchase_receipt").then(value =>{
			if(value==1){
				if(frm.doc.items.length){
					if(frm.doc.items[0].purchase_order){
						cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",0)
					}
					else{
						cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",1)
					}
				}
				else{
					cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",1)
				}
			}
			else{
				cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",1)
			}
		})
		var data=locals[cdt][cdn]
		for(var i=0;i<data.items.length;i++){
			item_codes.push(data.items[i].item_code)
		}
	},
	// supplier:function(frm,cdt,cdn){
	// 	var ts_data=locals[cdt][cdn]
	// 	var ts_supplier=ts_data.supplier
	// 	if(ts_supplier!=""){
	// 		frappe.call({
	// 			method:"sks.sks.custom.py.supplier_items_finder.ts_supplier_items_finder",
	// 			args:{ts_supplier},
	// 			callback(ts_r){
	// 				var ts_supplier_matched_item=ts_r["message"]
	// 				frm.set_query("item_code", "items", function() {
	// 					return {
	// 						query: "erpnext.controllers.queries.item_query",
	// 						filters: {'item_code' : ["in", ts_supplier_matched_item],'is_purchase_item': 1}
	// 					}
	// 				})
	// 			}
	// 		})
	// 	}
	// },
	scan_barcode_to_verify_the_items: function(frm,cdt,cdn){
		let data=locals[cdt][cdn]
		var search_value = data.scan_barcode_to_verify_the_items
		var checking_purchase_order = data.items[0].purchase_order
		var matched_count=0
		if(search_value !="")
		{
			frappe.call({
				method:"erpnext.selling.page.point_of_sale.point_of_sale.search_for_serial_or_batch_or_barcode_number",
				args:{search_value},
				callback(r){
					var item_code_checking = r["message"]["item_code"]
					frappe.call({
						method:"sks.sks.custom.py.purchase_receipt.item_check_with_purchase_order",
						args:{item_code_checking,checking_purchase_order},
						callback(r){
							for(var i=0;i<item_codes.length;i++){
								if(item_code_checking == item_codes[i] || item_code_checking==null){
									matched_count=matched_count+1
									if(r["message"]==0){
										var d = new frappe.ui.Dialog({
											title: __('Scanned Barcode is not matched with the items, So map the barcode with item'),
											fields: [
												{
													"label": "Barcode",
													"fieldname": "barcode",
													"fieldtype": "Data",
													"options":Barcode,
													"reqd": 1,
													"read_only":1,
													"default": search_value
												},
												{
													"label": "Item code",
													"fieldname": "item_code",
													"fieldtype": "Link",
													"filters": {'item_code' : ["in", item_codes]},
													"reqd": 1,
													"options":"Item"
												},
											],
											primary_action: function(data) {
												var barcode=data.barcode
												total_barcode_number_item.push(barcode)
												var item_code=data.item_code
												total_barcode_item_code.push(item_code)
												frappe.call({
													method:"sks.sks.custom.py.purchase_receipt.adding_barcode",
													args:{barcode,item_code},
												})
												d.hide();
												frappe.show_alert({ message: __('Barcode Mapped'), indicator: 'green' });
												frappe.model.set_value(cdt,cdn,"scan_barcode_to_verify_the_items","")
												d.hide();
											}
										});d.show()
									}
									else{
										for(var i=0;i<data.items.length;i++){
											if(r["message"]==data.items[i].item_code){
												frappe.model.set_value(data.items[i].doctype,data.items[i].name,"item_verified",1)
											}
										}
										frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
										frappe.model.set_value(cdt,cdn,"scan_barcode_to_verify_the_items","")
									}
									break
								}
							}
							if(matched_count==0){
								frappe.show_alert({ message: __('Barcode Already Exists'), indicator: 'red' });
							}
							matched_count=0
						}
					})
				}
			})
		}
		frm.set_value("scanned_items",JSON.stringify(total_barcode_item_code))
		frm.set_value("scanned_barcodes",JSON.stringify(total_barcode_number_item))
	}
})

// frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation").then(value =>{
// 	if(value==1){
// 		frappe.ui.form.on("Purchase Receipt",{
// 			after_save:function(frm,cdt,cdn){
// 				var data = locals[cdt][cdn]
// 				var doctype_name=data.doctype
// 				var document_name=data.name
// 				var expiry_date=[]
// 				var item_rate=[]
// 				var item_mrp=[]
// 				var item_code=[]
// 				for(var i=0;i<data.items.length;i++){
// 					var against_purchase_order_name=data.items[i].purchase_order
// 					expiry_date.push(data.items[i].expiry_date)
// 					item_rate.push(data.items[i].ts_valuation_rate)
// 					item_code.push(data.items[i].item_code)
// 					item_mrp.push(data.items[i].ts_mrp)
// 				}
// 				frappe.call({
// 					method:"sks.sks.custom.py.purchase_receipt.auto_batch_creation",
// 					args:{expiry_date,item_rate,item_code,item_mrp,total_barcode_number_item,total_barcode_item_code,against_purchase_order_name,doctype_name,document_name},
// 					callback(r){
// 						if(r["message"]==0){
// 							frm.refresh();
// 						}
// 					}
// 				})
// 			}
// 		})
// 	}
// })
frappe.ui.form.on("Purchase Receipt Item",{
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
			frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation").then(value =>{
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
	},
	is_free_item_from_supplier:function(frm,cdt,cdn){
		data=locals[cdt][cdn]
		if(data.is_free_item_from_supplier == 1){
			 var df=frappe.meta.get_docfield(cdt,"ts_selling_rate",cdn);
			 df.read_only=0;
			 frm.refresh_fields();
			 
		}else {
			var df=frappe.meta.get_docfield(cdt,"ts_selling_rate",cdn);
			df.read_only=1;
			frm.refresh_fields();
		}   
	},
})

