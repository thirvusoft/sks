// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Thirvu Supplier Quotation Comparison"] = {
	filters: [
		{
			fieldtype: "Link",
			label: __("Company"),
			options: "Company",
			fieldname: "company",
			default: frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			default: "",
			options: "Item",
			label: __("Item"),
			fieldname: "item_code",
			fieldtype: "Link",
			get_query: () => {
				let quote = frappe.query_report.get_filter_value('supplier_quotation');
				if (quote != "") {
					return {
						query: "erpnext.stock.doctype.quality_inspection.quality_inspection.item_query",
						filters: {
							"from": "Supplier Quotation Item",
							"parent": quote
						}
					}
				}
				else {
					return {
						filters: { "disabled": 0 }
					}
				}
			}
		},
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Supplier', txt);
			}
		},
		{
			fieldtype: "MultiSelectList",
			label: __("Supplier Quotation"),
			fieldname: "supplier_quotation",
			default: "",
			get_data: function(txt) {
				return frappe.db.get_link_options('Supplier Quotation', txt, {'docstatus': ["<", 2]});
			}
		},
		{
			fieldtype: "Link",
			label: __("Request for Quotation"),
			options: "Request for Quotation",
			fieldname: "request_for_quotation",
			default: "",
			get_query: () => {
				return { filters: { "docstatus": ["<", 2] } }
			}
		},
		{
			"fieldname":"group_by",
			"label": __("Group by"),
			"fieldtype": "Select",
			"options": [__("Group by Supplier"), __("Group by Item")],
			"default": __("Group by Supplier")
		},
		{
			fieldtype: "Check",
			label: __("Include Expired"),
			fieldname: "include_expired",
			default: 0
		}
	],
	
	formatter: (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);

		if(column.fieldname === "valid_till" && data.valid_till){
			if(frappe.datetime.get_diff(data.valid_till, frappe.datetime.nowdate()) <= 1){
				value = `<div style="color:red">${value}</div>`;
			}
			else if (frappe.datetime.get_diff(data.valid_till, frappe.datetime.nowdate()) <= 7){
				value = `<div style="color:darkorange">${value}</div>`;
			}
		}

		if(column.fieldname === "price_per_unit" && data.price_per_unit && data.min && data.min === 1){
			value = `<div style="color:green">${value}</div>`;
		}
		return value;
	},

	get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    },
	
	onload: (report) => {
		// Create a button for Creating Purchase Order
		frappe.query_report.page.add_inner_button(__("Confirm Supplier"), function() {
			var button = new frappe.ui.Dialog({
				size:"small",
				title: "Action",
				fields: [
					{label:'Create Purchase Order',fieldname:'create_po',fieldtype:'Select',options:['Purchase Order'],default:"Purchase Order",reqd:1},
					{label:'Required Date',fieldname:'required_date',fieldtype:'Date',reqd:1},
				],
				primary_action:function(data){
					var required_date = data.required_date
					create_po(required_date)
					button.hide()
				}
				
					})
					button.show()	
	});

	}
}

var create_po = function(required_date){	
	let checked_rows_indexes = frappe.query_report.datatable.rowmanager.getCheckedRows();
	let checked_rows = checked_rows_indexes.map(i => frappe.query_report.data[i]);
		var quotation_list = []
		for(var i=0;i<checked_rows.length;i++)
			{
				quotation_list.push(checked_rows[i].quotation)	
			}
			for(let i in quotation_list){
					frappe.call({
						method: "sks.sks.report.thirvu_supplier_quotation_comparison.thirvu_supplier_quotation_comparison.make_purchase_order",
						args: {
							source_name: quotation_list[i],
							r_date: required_date
						},
					});
			}
		}