// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Feedback Form', {
	refresh: function(frm) {
		let invoice_list = [];
		cur_frm.fields_dict.invoice_no.$input.on("click", function() {
			frappe.db.get_list("Customer Feedback Form",{fields:['invoice_no']}).then(function(data){
				for(let i of data){invoice_list.push(i['invoice_no'])}
				cur_frm.set_query('invoice_no',function(){
					return {
						filters:{
							'name': ['not in',invoice_list]
						}
					}
				})	
			})
			
		});		
	}
});
