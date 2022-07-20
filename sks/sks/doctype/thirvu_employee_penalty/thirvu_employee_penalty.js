// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt


frappe.ui.form.on('Thirvu Employee Penalty', {
	reason: function(frm) {
		if(frm.doc.reason == 'Late Entry'){
			frappe.db.get_single_value('Thirvu HR Settings', 'leave_penalty_amount').then((value) => {
			cur_frm.set_value('amount',value)
		})
	}
}
});
