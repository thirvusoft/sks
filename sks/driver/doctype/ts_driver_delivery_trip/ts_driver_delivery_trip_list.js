frappe.listview_settings['TS Driver Delivery Trip'] = {
	add_fields: ["driver", "status", "name"],
	filters: [["status", "=", "On Process"]],
    // filters: [["name", "=", frappe.session.user]],
	get_indicator: function(doc) {
		var colors = {
			"Open": "orange",
			"Hold": "red",
			"On Process": "blue",
			"Completed": "green",
			"Closed": "dark green",
		}
		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
	},
    // onload:function(listview){
    //     console.log("hi")
    //     filters= [["assigned_to", "=", frappe.session.user]]
    // }
	

};
