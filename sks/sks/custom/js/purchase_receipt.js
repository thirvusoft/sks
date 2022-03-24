frappe.ui.form.on("Purchase Receipt",{
	scan_barcode_to_verify_the_items: function(frm,cdt,cdn){
		let data=locals[cdt][cdn]
		var search_value = data.scan_barcode_to_verify_the_items
		var checking_purchase_order = data.items[0].purchase_order
		if(search_value !="")
		{
		frappe.call({
			method:"erpnext.selling.page.point_of_sale.point_of_sale.search_for_serial_or_batch_or_barcode_number",
			args:{search_value},
			callback(r){
				var item_code_checking = r["message"]["item_code"]
				frappe.call({
					 method:"sks.sks.custom.py.purchase_receipt.item_check_with_purchase_order",
					 args:{item_code_checking,checking_purchase_order},
					 callback(r){
						if(r["message"]==0){
							var d = new frappe.ui.Dialog({
								title: __('Scanned Barcode Is Not Matched With The Items, So Map The Barcode With Item'),
								fields: [
									{
										"label": "Barcode",
										"fieldname": "barcode",
										"fieldtype": "Data",
										"options":Barcode,
										"reqd": 1,
										"default": search_value
									},
									{
										"label": "Item code",
										"fieldname": "item_code",
										"fieldtype": "Link",
										"reqd": 1,
										"options":"Item"
									},
								],
								primary_action: function(data) {
									console.log(data.barcode)
									var barcode=data.barcode
									var item_code=data.item_code
									console.log(data.item_code)
									frappe.call({
										method:"sks.sks.custom.py.purchase_receipt.adding_barcode",
										args:{barcode,item_code},
									})
									frappe.show_alert({ message: __('Barcode Mapped'), indicator: 'green' });
									d.hide();
								}
							});d.show()
						}
						else{
							for(var i=0;i<data.items.length;i++){
								if(r["message"]==data.items[i].item_code){
									frappe.model.set_value(data.items[i].doctype,data.items[i].child_docname,"item_verified",1)
								}
							}
							frappe.show_alert({ message: __('Item Matched'), indicator: 'green' });
							frappe.model.set_value(cdt,cdn,"scan_barcode_to_verify_the_items","")
						}
					}
				})
			}
		})
		}
	}
})