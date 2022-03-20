var value=frappe.db.get_single_value("SKS Settings","allow_only_if_delivery_note_items_match_with_sales_order_items").then(value =>{
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
		frappe.model.set_value(cdt,cdn,"check_box",1)
		frappe.call({
			method:"erpnext.selling.page.point_of_sale.point_of_sale.search_for_serial_or_batch_or_barcode_number",
			args:{search_value},
			callback(r){
				var item_code_checking = r["message"]["item_code"]
				frappe.call({
				 	method:"sks.sks.custom.py.delivery_note_test_with_sales_order.item_check_with_sales_order",
				 	args:{item_code_checking,checking_sales_order},
					 callback(r){
						if(r["message"]==0){
							frappe.msgprint("Scanned Barcode Is Not Matching With The Sales Order Items")	
						}
						else{
							for(var i=0;i<data.items.length;i++){
								if(r["message"]==data.items[i].item_code){
									frappe.model.set_value(data.items[i].doctype,data.items[i].child_docname,"item_verified",1)
								}
							}
							frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
							frappe.model.set_value(cdt,cdn,"scan_barcode_to_verify_the_items","")
						}
					}
				})
			}
		})
		}
	}
})


frappe.ui.form.on("Delivery Note",{
	before_save: function(frm,cdt,cdn){
		var total_matched_items=0
		var not_verified_items=[]
		let data=locals[cdt][cdn]
		for(var i=0;i<data.items.length;i++){
			if(data.items[i].item_verified==0){
				not_verified_items=not_verified_items+data.items[i].item_name
				if(data.items.length != i+1){
					not_verified_items=not_verified_items+", "
				}
			}
			else{
				total_matched_items=total_matched_items+1
			}
		}
		if(total_matched_items!=data.items.length){
			frappe.throw(not_verified_items+" are not verified, please check it...")
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
