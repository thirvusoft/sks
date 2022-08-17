var data
var warehouse,parent_data
frappe.ui.form.on("Delivery Note",{
	onload:function(frm,cdt,cdn){
			parent_data=locals[cdt][cdn]
			if (parent_data.is_first_onload == 0){
				for(var i=0;i<parent_data.items.length;i++){
					frappe.model.set_value(parent_data.items[i].doctype,parent_data.items[i].name,"batch_no","")
				}
				frm.set_value("is_first_onload",1)
			}
	},
	sales_order: function(frm, cdt, cdn) {
		let outstanding_amount= locals[cdt][cdn]
		let outstanding_amount_and_total_amount=frappe.db.get_value("Sales Order", outstanding_amount.sales_order, ["outstanding_amount","outstanding_amount_and_total_amount"]).then(function(f){
		frappe.model.set_value(cdt,cdn, 'outstanding_amount',f.outstanding_amount)   
		frappe.model.set_value(cdt,cdn,'outstanding_amount_and_total_amount',f.message.outstanding_amount_and_total_amount)
		})
	}
})

frappe.db.get_single_value("Thirvu Retail Settings","allow_only_if_delivery_note_items_match_with_sales_order_items").then(value =>{
	if(value==1){
	// cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",0)
	frappe.ui.form.on("Delivery Note",{
		scan_barcode_to_verify_the_items: function(frm,cdt,cdn){
			let data=locals[cdt][cdn]
			var search_value = data.scan_barcode_to_verify_the_items
			var checking_sales_order = data.items[0].against_sales_order
			if(search_value !="")
			{
			frappe.call({
				method:"erpnext.selling.page.point_of_sale.point_of_sale.search_for_serial_or_batch_or_barcode_number",
				args:{search_value},
				callback(r){
					var item_code_checking = r["message"]["item_code"]
					frappe.call({
						 method:"sks.sks.custom.py.delivery_note.item_check_with_sales_order",
						 args:{item_code_checking,checking_sales_order,search_value},
						 callback(r){
							if(r["message"]==0){
								frappe.msgprint("Scanned Barcode Is Not Matching With The Sales Order Items")  
							}
							else{
								var ts_main,single_barcode=0,matched=0,new_total_item_count,j,new_length,item_code,against_sales_order,so_detail
								var length=data.items.length
								for(var i=0;i<length;i++){
									if(r["message"][0]==data.items[i].item_code){
										ts_main=data.items[i]
										if(r.message[1]){
											if((r.message[1]).length==1){
												single_barcode=1
												if(ts_main.is_batch_different_item == 0){
													var f=i
												}
												console.log(ts_main.batch_no,ts_main.batch_no,r.message[1][0],ts_main.is_batch_different_item)
												if (ts_main.batch_no == "" || ts_main.batch_no==r.message[1][0] && ts_main.is_batch_different_item == 0){
													console.log("1")
													matched=1
													frappe.model.set_value(data.items[i].doctype,data.items[i].name,"batch_no",r.message[1][0])
													frappe.model.set_value(data.items[i].doctype,data.items[i].name,"item_verified",1)
													var item_verified_count = ts_main.item_verified_count
													item_verified_count= item_verified_count+1
													frappe.model.set_value(data.items[i].doctype,data.items[i].name,"item_verified_count",item_verified_count)
													frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
													break
												}
												else if(ts_main.is_batch_different_item == 1 && ts_main.batch_no==r.message[1][0]){
													console.log("2")
													matched=1
													var item_verified_count = ts_main.item_verified_count
													item_verified_count= item_verified_count+1
													frappe.model.set_value(data.items[i].doctype,data.items[i].name,"item_verified_count",item_verified_count)
													frappe.model.set_value(data.items[i].doctype,data.items[i].name,"qty",item_verified_count)
													frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
													var item_count=data.items[f].qty
													item_count = item_count-1
													frappe.model.set_value(data.items[f].doctype,data.items[f].name,"qty",item_count)
													break
												}
												else {
													console.log("3")
													var total_item_count=ts_main.qty
													new_total_item_count = total_item_count-1
													j=i
													new_length=length
													against_sales_order = ts_main.against_sales_order
													so_detail=ts_main.so_detail
													item_code=ts_main.item_code
												}
											}
											else if((r.message[1]).length>1){
												var ts_batch_details=[]
												var ts_maping={}
												for (var j = 0; j < r.message[1].length; j++) {
													ts_batch_details.push("Batch No:- "+r.message[1][j]+  " |MRP:- " + r.message[2][j])
													ts_maping["Batch No:- "+r.message[1][j]+  " |MRP:- " + r.message[2][j]]=r.message[1][j]
												}
												let d = new frappe.ui.Dialog({
													title: 'Batch Selection',
													fields: [               
														{
															label: 'Batch No',
															fieldname: 'batch_no',
															fieldtype: "Select",
															options: ts_batch_details
														},
													],
													primary_action_label: 'OK',
													primary_action(values) {
														var batch_no = ts_maping[values["batch_no"]]
														if (ts_main.batch_no == "" || ts_main.batch_no==batch_no && ts_main.is_batch_different_item == 0){
														// frappe.model.set_value(ts_main.doctype,ts_main.name,"batch_no",batch_no)
														// frappe.model.set_value(ts_main.doctype,ts_main.name,"item_verified",1)
														// frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
															console.log("1")
															matched=1
															frappe.model.set_value(ts_main.doctype,ts_main.name,"batch_no",batch_no)
															frappe.model.set_value(ts_main.doctype,ts_main.name,"item_verified",1)
															var item_verified_count = ts_main.item_verified_count
															item_verified_count= item_verified_count+1
															frappe.model.set_value(ts_main.doctype,ts_main.name,"item_verified_count",item_verified_count)
															frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
														}
														d.hide();
													}
												});
												d.show();
											}
											else{
												frappe.model.set_value(data.items[i].doctype,data.items[i].name,"item_verified",1)
												frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
											}
										}
									}

								}
								if(matched==0 && single_barcode==1){
									console.log("3")
									frappe.model.set_value(data.items[j].doctype,data.items[j].name,"qty",new_total_item_count)
									frm.add_child("items",{
										
									})
									refresh_field("items");
									frappe.model.set_value(data.items[new_length].doctype,data.items[new_length].name,"item_code",item_code)
									frappe.model.set_value(data.items[new_length].doctype,data.items[new_length].name,"is_batch_different_item",1)
									frappe.model.set_value(data.items[new_length].doctype,data.items[new_length].name,"batch_no",r.message[1][0])
									frappe.model.set_value(data.items[new_length].doctype,data.items[new_length].name,"item_verified_count",1)
									frappe.model.set_value(data.items[new_length].doctype,data.items[new_length].name,"against_sales_order",against_sales_order)
									frappe.model.set_value(data.items[new_length].doctype,data.items[new_length].name,"so_detail",so_detail)
								}
								frappe.model.set_value(cdt,cdn,"scan_barcode_to_verify_the_items","")
							}
						}
					})
				}
			})
			}
		}
	})
	}
	else{
		// cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",1)
	}
 })
  

 frappe.ui.form.on("Delivery Note Item",{
	qty:function(frm,cdt,cdn){
		frappe.db.get_single_value("Thirvu Retail Settings","reserved_stock").then(value =>{
			if(value==1){
				var data = locals[cdt][cdn]
				var item_code=data.item_code
				var item_qty=data.qty
				var source_warehouse=data.warehouse
				frappe.call({
					method:"erpnext.stock.dashboard.item_dashboard.get_data",
					args:{item_code,warehouse:source_warehouse},
					callback(r){
						var projected_qty=r.message[0].projected_qty    
						if(item_qty>projected_qty){
							for(var i=0;i<parent_data.items.length;i++){
								if(item_code==parent_data.items[i].item_code){
									frappe.model.set_value(parent_data.items[i].doctype,parent_data.items[i].name,"qty",0)
									frappe.throw({
										title:"Stock Unavailable",
										message:"For Item : "+item_code+", The Quantity must be less than : "+projected_qty
									})
								}
							}
						}
					}
				})
			}
		})
	}
 })