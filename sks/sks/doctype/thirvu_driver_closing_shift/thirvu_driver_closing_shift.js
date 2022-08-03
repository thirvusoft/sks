// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Thirvu Driver Closing Shift', {
	on_submit:function(frm){
		frappe.call({
			method: "sks.sks.doctype.thirvu_driver_closing_shift.thirvu_driver_closing_shift.get_payment_details",
			args: {
				doc: frm.doc,
			},
			callback: function(r) {
				if(r.message.length != 0){
					var d = new frappe.ui.Dialog({
						size: "large",
						title:"Choose Account Head",
						fields:[
						{fieldname:'account_details', fieldtype:'Table',cannot_add_rows: 1,in_place_edit: true, fields:[
						{
							label: 'Mode of Payment',
							fieldname: 'mode_of_payment',
							fieldtype: 'Read Only',
							in_list_view:1,
							read_only:1,
							columns:2
						},
						{
							label: 'Amount',
							fieldname: 'amount',
							fieldtype: 'Read Only',
							in_list_view:1,
							read_only:1,
							columns:2
						},
						{
							label: 'Debit Account Head',
							fieldname: 'debit_account_head',
							fieldtype: 'Read Only',
							in_list_view:1,
							read_only:1,
							columns:2,
						},
						{
							label: 'Credit Account Head',
							fieldname: 'credit_account_head',
							fieldtype: 'Link',
							options:"Account",	
							in_list_view:1,
							columns:2
						},
						],
						  data:r.message},
						],
						primary_action : function(data){
							for (let value in data.account_details){
								if(!data.account_details[value].credit_account_head){
									frappe.throw({message:__("Please select Credit Account for "+ data.account_details[value].mode_of_payment ), title: __("Mandatory")});
								}
							}
							frappe.call({
								method: "sks.sks.doctype.thirvu_driver_closing_shift.thirvu_driver_closing_shift.create_journal_entry",
								args: {
									data: data,
									doc:frm.doc
								},
								callback:function(data){
									if(data.message == 1){
										frappe.show_alert({ message: __('Journal Entry Created Successfully.'), indicator: 'green' });
	
									}
								}
							})
						d.hide();
						},
						primary_action_label: __('Create Journal Entry')
					});
			  d.show();
				}
		}
	});
	},
});
