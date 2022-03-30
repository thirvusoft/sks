frappe.db.get_single_value("SKS Settings","allow_only_if_sales_invoice_items_match_with_sales_order_items").then(value =>{
	if(value==1){
	cur_frm.set_df_property("scan_barcode","hidden",1)
	cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",0)
	frappe.ui.form.on("Sales Invoice",{
		scan_barcode_to_verify_the_items: function(frm,cdt,cdn){
			let data=locals[cdt][cdn]
			if(data.update_stock==1){
				var search_value = data.scan_barcode_to_verify_the_items
				var checking_sales_invoice = data.items[0].sales_order
				if(search_value !="")
				{
					frappe.call({
						method:"erpnext.selling.page.point_of_sale.point_of_sale.search_for_serial_or_batch_or_barcode_number",
						args:{search_value},
						callback(r){
							var item_code_checking = r["message"]["item_code"]
							frappe.call({
								method:"sks.sks.custom.py.sales_invoice.item_check_with_sales_order",
								args:{item_code_checking,checking_sales_invoice},
								callback(r){
									if(r["message"]==0){
										frappe.msgprint("Scanned Barcode Is Not Matching With The Sales Order Items")  
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
								}
							})
						}
					})
				}
			}
		}
	})
	frappe.ui.form.on("Sales Invoice",{
		before_save: function(frm,cdt,cdn){
			var data=locals[cdt][cdn]
			if(data.update_stock==1){
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
		}
	})
	}
	else{
		cur_frm.set_df_property("scan_barcode","hidden",0)
		cur_frm.set_df_property("scan_barcode_to_verify_the_items","hidden",1)
		frappe.ui.form.on("Sales Invoice Item",{
			item_code:function(frm,cdt,cdn){
				// var df=frappe.meta.get_docfield("Sales Invoice Item","item_code",frm.doc.name);
				// df.read_only=1;
				// var df=frappe.meta.get_docfield("Sales Invoice Item","qty",frm.doc.name);
				// df.read_only=1;
				// frm.get_docfield("items", "item_verified").hidden = 1;
				// // console.log("gggggggggggggggggggggggggg")
				// // // if(cur_frm.get_field("items")){
				// // // hide_field(["items"]["item_verified"]);}
				// // var df=frappe.meta.get_docfield(cdt,"item_verified",cdn);
				// // df.hidden=1;
				// frm.refresh_fields();
				// frm.refresh_field("items");
				// // console.log(df)
				// // frm.set_df_property("item_verified","hidden",1)
			}
		})
	}
 })
	// console.log("kkkkkkkkkkkkkkkkkk")
	// frappe.ui.form.on("Sales Invoice",{
	//  before_load:function(frm) {
	//  console.log("gggggggggggggggggggggggggg")
	//  var df=frappe.meta.get_docfield("Sales Invoice Item","rate",frm.doc.name);
	//  df.hidden=1;
	//  frm.refresh_fields();
	//  }
	// });
	// cur_frm.items.set_df_property("item_verified","hidden",0)
	// cur_frm.get_field("items").grid.fieldinfo["item_verified"].hidden = 0
	// var df = frappe.meta.get_docfield("items","item_verified", cur_frm.doc.name);
	// var d1 =  {  
	//  "field_name": "Item_verified"
	// }
   
	// frappe.call({
	// args: d1,
	//   method: "sks.sks.custom.py.sales_invoice_test_with_sales_order.property",
	//   callback: function(r)
	// { }})
	// df.hidden = 1;
	// var df = frappe.meta.get_docfield("Chid DocType", fieldname , cur_frm.doc.name);
	// df.hidden = 1;
	// console.log(df)
	// var df = frappe.meta.get_docfield("Sales Invoice Item",item_verified , cur_frm.doc.name);
	// df.hidden = 1;
	// df.set_df_property("item_verified","hidden",0)
	// b=frappe.db.get_doc("Sales Invoice Item")
	// console.log(b)
	// set_df_property("Sales Invoice Item","item_verified","hidden",0)

 var parent_data
 frappe.ui.form.on("Sales Invoice",{
	onload:function(frm,cdt,cdn){
		parent_data=locals[cdt][cdn]
	}
 })
 frappe.ui.form.on("Sales Invoice Item",{
	qty:function(frm,cdt,cdn){
		frappe.db.get_single_value("SKS Settings","reserved_stock").then(value =>{
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
 





// frappe.ui.form.on("Sales Invoice",{
// 	before_save:function(frm,cdt,cdn){
// 		frappe.call({
// 			method:"sks.sks.custom.py.sales_invoice_test_with_sales_order.payment_entry",
// 			// args:{
// 			// // amount,mode,customer,pending_invoice
			
// 			// 	amount:data.amount,
// 			// 	mode:data.mode,
// 			// 	customer:customer,
// 			// 	pending_invoice:r.message[1],
// 			// 	company:_vm._data.pos_profile.company.company_name,
// 			// 	ref_no: data.ref_no,
// 			// 	ref_date: data.ref_date
				
// 			// },
// 			// callback : function(res){
// 			// 	if(res.message[0]){
// 			// 		evntBus.$emit('show_mesage', {
// 			// 		text: __('Payment Entry Created Successfully.'),
// 			// 		color: 'success',
// 			// 		});
// 			// 		var mode = r.message[1]
// 			// 		var payment = r.message[0]
			
// 			// 	}
// 			// }
// 		})
// 	}
// })


var loop
frappe.ui.form.on("Sales Invoice",{
    onload:function(){
        loop=0
    }
})
frappe.ui.form.on("Sales Invoice",{
	after_save:function(frm,cdt,cdn){
		frappe.db.get_single_value("SKS Settings","credit_bill_history").then(value =>{
            if(value==1){
				if(cur_frm.doc.docstatus!=1){
					if(loop==0){
						var data1 = locals[cdt][cdn]
						var customer = data1.customer
						frappe.call({
							method : "sks.sks.custom.py.sales_order.customer_credit_sale",
							args:{
								customer: customer
							},
							callback : function(r){
								if(r.message[2]>0){
									var d = new frappe.ui.Dialog({
										size: "extra large",
										title:"Customer: "+ customer +"'s Outstanding Amount",
										fields:[
											{'fieldname':'alert','fieldtype':'HTML','read_only':1,'bold':1},
											{'label':'Outstanding Amount','fieldname':'outstanding','fieldtype':'Currency','default':r.message[2],'read_only':1},
											{'label':'Paid Amount','fieldname':'amount','fieldtype':'Currency','reqd':1},
											{
											'label':'Mode of Payment',
											'fieldname':'mode',
											'fieldtype':'Link',
											'options':"Mode of Payment"
											},
											{'label':'Reference Date','fieldname':'ref_date','fieldtype':'Date'},
											{'label':'Reference Number','fieldname':'ref_no','fieldtype':'Data'}
											
										],
										primary_action : function(data){
											loop=loop+1
											frappe.call({
												method:"sks.sks.custom.py.sales_invoice.payment_entry",
												args:{
													amount:data.amount,
													mode:data.mode,
													customer:customer,
													pending_invoice:r.message[1],
													company:frm.doc.company,
													ref_no: data.ref_no,
													ref_date: data.ref_date	
												},
												callback : function(res){
													if(res.message[0]){
														frappe.show_alert({ message: __('Payment Entry Created Successfully.'), indicator: 'green' });
													}
												}
											});d.hide();
										}
									});
								}
								var template = r.message[3]
								d.set_df_property('alert','options',frappe.render(template,{}))
								d.show();
							}
						})
					}
				}
			}
		})
	}
})
	