// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt

let company;
var driver_id;
var driver_name;
var creation_datetime;
var submit = false;
var doc_name
frappe.ui.form.on('TS Driver Delivery Trip', {
	setup: function(frm,cdt,cdn) {
		company = frm.doc.company;
		driver_id=frm.doc.driver_id;
		driver_name=frm.doc.driver
		creation_datetime=frm.doc.creation
		update_fields(frm,cdt,cdn)
	},
	before_submit: function(frm,cdt,cdn){
		if (submit){
			return
		}
		frappe.validated=false
		if(frm.doc.status=="Closed"){
			frappe.call({
				method:"sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.get_fields_for_denomination",
				args:{driver_id},
				callback(r){
				var d = new frappe.ui.Dialog({
					title: "Thirvu Driver Closing Shift",
					fields:[{
					
					label:"Denomination",fieldname:"ts_denomination",fieldtype:"Table",cannot_add_rows: 1,in_place_edit: true,ts_block:"Yes",fields:[
						{
						label: 'Amount',
						fieldname: 'currency',
						fieldtype: 'Read Only',
						in_list_view:1,
						columns:4,
						},
						{
						label: 'Count',
						fieldname: 'count',
						fieldtype: 'Int',
						default:0,
						in_list_view:1,
						columns:2,
								},
					],data:r.message[0],
					},
					{label:"Mode of Payments",fieldname:"ts_mode_of_payment",fieldtype:"Table",cannot_add_rows:1,in_place_edit: true,ts_block:"Yes",fields:[
						{
						label: 'Type',
						fieldname: 'ts_type',
						fieldtype: 'Read Only',
						in_list_view:1,
						columns:4,
								},
						{
						label: 'Amount',
						fieldname: 'currency',
						fieldtype: 'Currency',
						in_list_view:1,
						columns:2,
								},
					],data:r.message[1]
					}],
					primary_action_label:"Submit",
					primary_action: function(ts_denomination){
						frappe.call({
							method: "sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.create_driver_closing_shift",
							args:{
								ts_denomination,driver_name,creation_datetime,driver_id,doc_name
								},
							callback:function(thirvu_dcs){
								frm.set_df_property("status", "read_only",1);
								d.hide()
								frappe.show_alert({ message: __("Thirvu Driver Closing Shift Created Successfully"), indicator: 'green' });
								frappe.validated=true
								submit=true
								cur_frm.save("Submit")
								var difference=thirvu_dcs.message[0]
								if (thirvu_dcs.message[1] > thirvu_dcs.message[0]) {
									frappe.msgprint({
										message: __("Your responsible for the difference amount of rupees "+difference ),
										title: __('Payment Shortage')
									});
								} 

							}
						})	
					}
				});
				d.show()
				
				}
			})
		}
		else if(frm.doc.status!="Closed"){
			frappe.throw({title: "Message", message: "Kindly move the document to closed state!"})
		}
		update_fields(frm,cdt,cdn)
	},
	after_save:function(frm,cdt,cdn){
		doc_name=frm.doc.name
	},
	validate:function(frm,cdt,cdn){
		// frappe.validated=false
		update_fields(frm,cdt,cdn)	
	},
});
function update_fields(frm,cdt,cdn) {
	let k=0;
	frappe.call({
		method: "sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.get_buttons_data",
		args:{
			delivery_trip: frm.doc.delivery_trip
		},
		callback(r){
			frm.set_value("invoice_details",[])
			for(let i of r.message)
			{
				let p=locals[cdt][cdn]

				cur_frm.add_child("invoice_details")
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"sales_invoice",i.sales_invoice)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"status",i.delivery_status)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"customer",i.customer)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"customer_address",i.customer_address)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"reason",i.reason)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"contact",i.contact_person)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"time_of_delivery",i.time)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"amount",i.amount)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"delivery_trip",frm.doc.delivery_trip)
				frappe.model.set_value(p.invoice_details[k].doctype,p.invoice_details[k].name,"file_attachment",i.file_attachment)
				cur_frm.refresh_field('invoice_details')
				k=k+1
			}
		}
	})
}
frappe.ui.form.on("TS Invoice Delivery Trip",{
    'details': function(frm,cdt,cdn){
        let p = locals[cdt][cdn]
        if(p.sales_invoice)
		{
			let reason=p.reason
			if(reason == ""){reason = " "}
			let amount=p.amount
			if(amount == 0){amount = "0"}
			var today = new Date();
			var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
			frappe.call({
				method:"sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.driver_mode_of_payments",
				args:{driver_id:driver_id},
				callback(thirvu_mode_of_payments){
					var d = new frappe.ui.Dialog({
						title: "Invoice: " + p.sales_invoice,
						fields: [
						{fieldname: 'sales_invoice',label: 'Invoice',fieldtype: 'Link', default:p.sales_invoice, read_only: 1,options:'Sales Invoice'},
						{fieldtype:'Column Break'},
						{fieldname: 'customer',label: 'Customer',fieldtype: 'Link', default:p.customer, read_only: 1,options:'Customer'},
						{fieldtype:'Column Break'},
						{fieldname: 'dis_amount',label: 'Amount',fieldtype: 'Currency', default:amount, read_only: 1},
						{fieldtype:'Section Break'},
						{fieldname: 'address',fieldtype: 'HTML', read_only: 1,options:"<b>Address</b><br>"+p.customer_address},
						{fieldtype:'Column Break'},
						{fieldname: 'dis_reason',label: 'Reason',fieldtype: 'Data', default:p.reason, read_only: 1},
						{fieldtype:'Section Break',label: "Update Status"},
						{fieldname: 'delivery_status',label: 'Delivery Status',fieldtype: 'Select', options: ['Attempt','Delivered','Not Delivered','Ready To Dispatch', 'Reattempt','Returned'], default:p.status,},
						{fieldtype:'Column Break'},
						{fieldname: 'reason',label: 'Reason',fieldtype: 'Link', default:reason, options : 'Reason'},
						{fieldtype:'Column Break'},
						{fieldname: 'file_attachment',label: 'File Attach',fieldtype: 'Attach Image', default:p.file_attachment},
						{fieldtype:'Section Break', depends_on: "eval:doc.delivery_status == 'Delivered' "},
						{fieldname: 'mode_of_payment',label: 'Mode of Payment',fieldtype: 'Link',options: 'Mode of Payment',
						"get_query": function(){
							return{
								filters:[
									["name", "in" ,thirvu_mode_of_payments.message]
								]
									
							}
						}
						},
						{fieldtype:'Column Break'},
						{fieldname: 'amount',label: 'Paid Amount',fieldtype: 'Currency'},
						{fieldtype:'Column Break'},
						{fieldname: 'time_of_delivery',label: 'Time of Delivery',fieldtype: 'Time', default:time},
						{fieldtype:'Section Break'},
			
					],
					primary_action_label: "Update Invoice",
					primary_action:async function(data){

					await frappe.db.get_doc('Customer',data.customer,'is_credit_customer' ).then( (is_credit) => {
						if (is_credit.is_credit_customer == 0){
							if(data.amount > data.dis_amount){
								frappe.throw({title: "Message", message: "Paid Amount is more than Amount"})
							}
							else if (data.amount != data.dis_amount){
								frappe.throw({title: "Message", message: "The Customer is not credit customer"})
							}
						} 
					} )
				
					if(data.mode_of_payment && data.amount && data.sales_invoice && data.delivery_status == "Delivered"){					
						frappe.call({
							method:"sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.payment_entry",
							args:{
								mode: data.mode_of_payment,
								amount: data.amount,
								pending_invoice: data.sales_invoice,
								company: company,
								driver_id:driver_id
							},
							callback(res){
								// update_fields(frm,cdt,cdn)
								frappe.show_alert({
									message: res.message[0],
									indicator: res.message[1]
								});
								if(res.message[1] == 'red'){
									frappe.throw({
									title: "Amount Exceed",
									message: "Paid Amount is greater than the Outstanding Amount. ("+res.message[2]+" > "+res.message[3]+")"
									})
								}
							}
						})
					}
					frappe.call({
						method: "sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.update_values",
						args:{
							invoice: p.sales_invoice,
							fields: data,
							value:p.delivery_trip
							},
						callback(res){
							// update_fields(frm,cdt,cdn)
						}
					})
					if(!data.mode_of_payment) {
						frappe.throw(__("Please select Mode of Payment"));
					}
					d.hide();
					}
				})
				d.show();
				}		
			})
			
		}
	}
})
