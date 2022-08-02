var warehouse,parent_data,loop,company
frappe.ui.form.on("Sales Invoice",{
    company:function(frm,cdt,cdn){
        company=cur_frm.doc.company
    },
	onload:function(frm,cdt,cdn){
		parent_data=locals[cdt][cdn]
		loop=0
		if(cur_frm.doc.items[0].delivery_note){
			frm.set_df_property('update_stock', 'hidden', 1);
		}
		var day = new Date(cur_frm.doc.due_date);
		var weekdays=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
		cur_frm.set_value("due_day",weekdays[day.getDay()])
	},
	due_date:function(frm,cdt,cdn){
		var day = new Date(cur_frm.doc.due_date);
		var weekdays=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
		cur_frm.set_value("due_day",weekdays[day.getDay()])
	},
	after_save:function(frm,cdt,cdn){
		frappe.db.get_single_value("Thirvu Retail Settings","credit_bill_history").then(value =>{
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
								if(r.message[2]>0 && frm.doc.mode_of_delivery == 'Pick up'){
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
											'options':"Mode of Payment",
											'reqd':1
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

 frappe.ui.form.on("Sales Invoice Item",{
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
