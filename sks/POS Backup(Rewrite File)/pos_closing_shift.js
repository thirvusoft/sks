// Copyright (c) 2020, Youssef Restom and contributors
// For license information, please see license.txt

frappe.ui.form.on('POS Closing Shift', {
	onload: function (frm) {
		frm.set_query("pos_profile", function (doc) {
			return {
				filters: { 'user': doc.user }
			};
		});

		frm.set_query("user", function (doc) {
			return {
				query: "posawesome.posawesome.doctype.pos_closing_shift.pos_closing_shift.get_cashiers",
				filters: { 'parent': doc.pos_profile }
			};
		});

		frm.set_query("pos_opening_shift", function (doc) {
			return { filters: { 'status': 'Open', 'docstatus': 1 } };
		});

		if (frm.doc.docstatus === 0) frm.set_value("period_end_date", frappe.datetime.now_datetime());
		if (frm.doc.docstatus === 1) set_html_data(frm);
	},
	on_submit:function(frm){
		frappe.call({
			method: "posawesome.posawesome.api.posapp.get_payment_details",
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
							method: "posawesome.posawesome.api.posapp.create_journal_entry",
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
	pos_opening_shift (frm) {
		if (frm.doc.pos_opening_shift && frm.doc.user) {
			reset_values(frm);
			frm.trigger("set_opening_amounts");
			frm.trigger("get_pos_invoices");
		}
	},

	set_opening_amounts (frm) {
		frappe.db.get_doc("POS Opening Shift", frm.doc.pos_opening_shift)
			.then(({ balance_details }) => {
				balance_details.forEach(detail => {
					frm.add_child("payment_reconciliation", {
						mode_of_payment: detail.mode_of_payment,
						opening_amount: detail.amount || 0,
						expected_amount: detail.amount || 0
					});
				});
			});
	},

	get_pos_invoices (frm) {
		frappe.call({
			method: 'posawesome.posawesome.doctype.pos_closing_shift.pos_closing_shift.get_pos_invoices',
			args: {
				pos_opening_shift: frm.doc.pos_opening_shift,
			},
			callback: (r) => {
				let pos_docs = r.message;
				set_form_data(pos_docs, frm);
				refresh_fields(frm);
				set_html_data(frm);
			}
		});
	}
});

frappe.ui.form.on('POS Closing Shift Detail', {
	closing_amount: (frm, cdt, cdn) => {
		const row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "difference", flt(row.expected_amount - row.closing_amount));
	}
});

function set_form_data (data, frm) {
	data.forEach(d => {
		add_to_pos_transaction(d, frm);
		frm.doc.grand_total += flt(d.grand_total);
		frm.doc.net_total += flt(d.net_total);
		frm.doc.total_quantity += flt(d.total_qty);
		add_to_payments(d, frm);
		add_to_taxes(d, frm);
	});
}

function add_to_pos_transaction (d, frm) {
	frm.add_child("pos_transactions", {
		sales_invoice: d.name,
		posting_date: d.posting_date,
		grand_total: d.grand_total,
		customer: d.customer
	});
}

function add_to_payments (d, frm) {
	d.payments.forEach(p => {
		const payment = frm.doc.payment_reconciliation.find(pay => pay.mode_of_payment === p.mode_of_payment);
		if (payment) {
			let amount = p.amount;
			let cash_mode_of_payment = get_value("POS Profile", frm.doc.pos_profile, 'posa_cash_mode_of_payment');
			if (!cash_mode_of_payment) {
				cash_mode_of_payment = 'Cash';
			}
			if (payment.mode_of_payment == cash_mode_of_payment) {
				amount = p.amount - d.change_amount;
			}
			payment.expected_amount += flt(amount);
		} else {
			frm.add_child("payment_reconciliation", {
				mode_of_payment: p.mode_of_payment,
				opening_amount: 0,
				expected_amount: p.amount || 0
			});
		}
	});
}

function add_to_taxes (d, frm) {
	d.taxes.forEach(t => {
		const tax = frm.doc.taxes.find(tx => tx.account_head === t.account_head && tx.rate === t.rate);
		if (tax) {
			tax.amount += flt(t.tax_amount);
		} else {
			frm.add_child("taxes", {
				account_head: t.account_head,
				rate: t.rate,
				amount: t.tax_amount
			});
		}
	});
}

function reset_values (frm) {
	frm.set_value("pos_transactions", []);
	frm.set_value("payment_reconciliation", []);
	frm.set_value("taxes", []);
	frm.set_value("grand_total", 0);
	frm.set_value("net_total", 0);
	frm.set_value("total_quantity", 0);
}

function refresh_fields (frm) {
	frm.refresh_field("pos_transactions");
	frm.refresh_field("payment_reconciliation");
	frm.refresh_field("taxes");
	frm.refresh_field("grand_total");
	frm.refresh_field("net_total");
	frm.refresh_field("total_quantity");
}

function set_html_data (frm) {
	frappe.call({
		method: "get_payment_reconciliation_details",
		doc: frm.doc,
		callback: (r) => {
			frm.get_field("payment_reconciliation_details").$wrapper.html(r.message);
		}
	});
}

const get_value = (doctype, name, field) => {
	let value;
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': doctype,
			'filters': { 'name': name },
			'fieldname': field
		},
		async: false,
		callback: function (r) {
			if (!r.exc) {
				value = r.message[field];
			}
		}
	});
	return value;
};