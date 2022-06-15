// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt

let company;
frappe.ui.form.on('TS Driver Delivery Trip', {
	setup: function(frm,cdt,cdn) {
		company = frm.doc.company;
		update_fields(frm,cdt,cdn)
	},
	validate: function(frm,cdt,cdn) {
		update_fields(frm,cdt,cdn)
	},
	on_submit: function(frm,cdt,cdn) {
		update_fields(frm,cdt,cdn)
	}
});
function update_fields(frm,cdt,cdn) {
	let k=0;
	frappe.call({
		method: "sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.get_buttons_data",
		args:{
			delivery_trip: frm.doc.delivery_trip
		},
		callback(r){
			console.log(r.message)
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
				{fieldname: 'delivery_status',label: 'Delivery Status',fieldtype: 'Select', options: ['Attempt','Delivered','Not Delivered','Ready To Dispatch', 'Reattempt','Returned'], default:p.status},
				{fieldtype:'Column Break'},
				{fieldname: 'reason',label: 'Reason',fieldtype: 'Link', default:reason, options : 'Reason'},
				{fieldtype:'Column Break'},
				{fieldname: 'file_attachment',label: 'File Attach',fieldtype: 'Attach Image', default:p.file_attachment},
				{fieldtype:'Section Break'},
				{fieldname: 'mode_of_payment',label: 'Mode of Payment',fieldtype: 'Link',options: 'Mode of Payment',default: 'Cash'},
				{fieldtype:'Column Break'},
				{fieldname: 'amount',label: 'Paid Amount',fieldtype: 'Currency'},
				{fieldtype:'Column Break'},
				{fieldname: 'time_of_delivery',label: 'Time of Delivery',fieldtype: 'Time', default:time},
				{fieldtype:'Section Break'},
	
			],
			primary_action_label: "Update Invoice",
			primary_action: function(data){
		
			if(data.mode_of_payment && data.amount && data.sales_invoice && data.delivery_status == "Delivered"){
				frappe.call({
					method:"sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.payment_entry",
					args:{
						mode: data.mode_of_payment,
						amount: data.amount,
						pending_invoice: data.sales_invoice,
						company: company,
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
			d.hide();
			}
		})
		d.show()
		}
	}
})
