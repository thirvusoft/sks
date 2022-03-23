frappe.db.get_single_value("SKS Settings","allow_only_if_delivery_note_items_match_with_sales_order_items").then(value =>{
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

var parent_data
frappe.ui.form.on("Delivery Note",{
    onload:function(frm,cdt,cdn){
        parent_data=locals[cdt][cdn]
    }
})
frappe.ui.form.on("Delivery Note Item",{
    qty:function(frm,cdt,cdn){
		frappe.db.get_single_value("SKS Settings","reserved_stock").then(value =>{
			if(value==0){
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