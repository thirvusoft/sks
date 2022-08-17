frappe.listview_settings['Sales Invoice'] = {
	onload: function(listview) {
		listview.page.clear_menu()
		listview.page.add_menu_item(__("Create Sales Invoice"), function() {
			var d = new frappe.ui.Dialog({
				title: "Choose A Filter To Bill The Orders",
				fields: [
					{
						label:"Mode Of Delivery",
						fieldname:"mode_of_delivery",
						fieldtype:"Select",
						options:"\nPick Up\nDoor Delivery\nIs Local Delivery",
						reqd: 1,
						onchange: async function(){
							let delivery_type=d.get_value('mode_of_delivery')
							if (delivery_type == "Is Local Delivery"){
								d.set_df_property('delivery_day', 'hidden', 1)
								d.set_df_property('delivery_day', 'reqd', 0)
							}
							else{
								d.set_df_property('delivery_day', 'hidden', 0)
								d.set_df_property('delivery_day', 'reqd', 1)
							}
						}
					},
					{
						label:'Please Select Delivery Day',
						fieldname:'delivery_day',
						fieldtype:'Select',
						options:'\nSunday\nMonday\nTuesday\nWednesday\nThursday\nFriday\nSaturday',
						hidden:1
					}
				],
				primary_action_label: "Submit",
				primary_action: function(data){
					frappe.call({
						method: "sks.sks.custom.py.sales_invoice.delivery_note_to_sales_invoice",
						args: {data:data},
						callback(msg){
							frappe.msgprint(msg);
						}
					})
					d.hide();  
				}
			})
			d.show()   
		}).addClass("btn-warning").css({'color':'white','background-color': '#008000'});
  
	}
 };
 