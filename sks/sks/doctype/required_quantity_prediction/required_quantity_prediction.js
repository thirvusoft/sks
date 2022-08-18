// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Required Quantity Prediction', {
	find_required_quantity:function(frm,cdn,cdt){
		frappe.call({
			method:"sks.sks.doctype.required_quantity_prediction.required_quantity_prediction.required_quantity_prediction",
			args:{data:frm.doc},
			callback(r){
				frm.set_value("needed_quantity",r.message)
			}
		})
	}
});
