frappe.listview_settings['Delivery Note'] = {
    onload: function(listview) {
		listview.page.clear_menu()
		listview.page.add_menu_item(__("Create Delivery Notes"), function() {
			var d = new frappe.ui.Dialog({
				title: "Choose Delivery Day",
				fields: [
					{label:'Delivery Day',fieldname:'sec',fieldtype:'Section Break'},
					{label:'Day',fieldname:'day',fieldtype:'Select', options:'\nSunday\nMonday\nTuesday\nWednesday\nThursday\nFriday\nSaturday', reqd: 1},
				],
				primary_action_label: "Submit",
				primary_action: function(data){
					data = data
					frappe.call({
						method: "sks.sks.custom.py.delivery_note.sales_order_to_delivery_note",
						args: {
							day: data["day"]
						},
						callback(msg){
							frappe.msgprint(msg);
						}
					})
					d.hide();	
				}
			})
			d.show()	
		}).addClass("btn-warning").css({'color':'white','background-color': '#2490EF'});

	}
};