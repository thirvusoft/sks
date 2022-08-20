// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Thirvu Item Label Generator', {
	setup: function(frm){
		frm.set_query("batch_id", function () {
			return {
				filters: { 'item': frm.doc.item ,'disabled':0}
			};
		})
	},
	after_save: function(frm){
		frm.set_df_property("item", "read_only",1);
	},
	item: function(frm){
		frm.set_value("batch_id","")
		frm.set_value("barcode","")
		frm.set_value("label_barcode","")
		frm.set_value("ts_mrp","")
		frm.set_value("ts_selling_price","")
		frm.set_value("expiry_date","")
	},
	batch_id: function(frm){
		if(frm.doc.barcode){
			frm.set_value("label_barcode",frm.doc.barcode)
		}
	}
});
