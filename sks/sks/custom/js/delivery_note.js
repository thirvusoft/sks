var company 
var data
var warehouse
frappe.ui.form.on("Delivery Note",{
    company:function(frm,cdt,cdn){
        company=cur_frm.doc.company
        
        
    }
})

frappe.db.get_single_value("Thirvu Retail Settings","allow_only_if_delivery_note_items_match_with_sales_order_items").then(value =>{
	if(value==1){
	cur_frm.set_df_property("scan_barcode","hidden",1)
	cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",0)
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
								for(var i=0;i<data.items.length;i++){
									if(r["message"][0]==data.items[i].item_code){	
										var ts_main=data.items[i]
										if(r.message[1]){
											if((r.message[1]).length==1){
												frappe.model.set_value(data.items[i].doctype,data.items[i].name,"batch_no",r.message[1][0])
												frappe.model.set_value(data.items[i].doctype,data.items[i].name,"item_verified",1)
												frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
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
														frappe.model.set_value(ts_main.doctype,ts_main.name,"batch_no",ts_maping[values["batch_no"]])
														frappe.model.set_value(ts_main.doctype,ts_main.name,"item_verified",1)
														frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
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
		cur_frm.set_df_property("scan_barcode","hidden",0)
		cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",1)
		frappe.ui.form.on("Delivery Note Item",{
			onload:function(frm,cdt,cdn){
				// frm.get_docfield("items", "item_verified").hidden = 1;
				// // console.log("gggggggggggggggggggggggggg")
				// // // if(cur_frm.get_field("items")){
				// // // hide_field(["items"]["item_verified"]);}
				// // var df=frappe.meta.get_docfield(cdt,"item_verified",cdn);
				// // df.hidden=1;
				// // // frm.refresh_fields();
				// frm.refresh_field("items");
				// // console.log(df)
				// // frm.set_df_property("item_verified","hidden",1)
			}
		})
	}
 })
  
 var parent_data
 frappe.ui.form.on("Delivery Note",{
	onload:function(frm,cdt,cdn){
		parent_data=locals[cdt][cdn]
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

 frappe.ui.form.on("Delivery Note",{
	onload:function(frm,cdt,cdn){
		var day = new Date(cur_frm.doc.posting_date);
		var weekdays=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
		cur_frm.set_value("posting_day",weekdays[day.getDay()])
	}
 })

 
 frappe.ui.form.on('Delivery Note', {
    sales_order: function(frm, cdt, cdn) {
    let outstanding_amount= locals[cdt][cdn]
    let outstanding_amount_and_total_amount=frappe.db.get_value("Sales Order", outstanding_amount.sales_order, ["outstanding_amount","outstanding_amount_and_total_amount"]).then(function(f){
    frappe.model.set_value(cdt,cdn, 'outstanding_amount',f.outstanding_amount)   
    frappe.model.set_value(cdt,cdn,'outstanding_amount_and_total_amount',f.message.outstanding_amount_and_total_amount)
   
    })
}
})

frappe.ui.form.on("Delivery Note Item",{
	item_code:function(frm,cdt,cdn){
			data=locals[cdt][cdn]
			var item_code=data.item_code
				if(item_code){
					frappe.call({
						method:"sks.sks.custom.py.delivery_note.item_warehouse_fetching",
						args:{item_code,company},
						callback(r){
								frappe.model.set_value(data.doctype, data.name, "warehouse", r.message)
								frappe.model.set_value(data.doctype, data.name, "ts_warehouse", r.message)
								warehouse=cur_frm.doc.ts_warehouse
						}
					})
					
				}
				
				
		},
		
	
		})	