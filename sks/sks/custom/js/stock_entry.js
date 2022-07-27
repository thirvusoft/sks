frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation").then(value =>{
	if(value==1){
		frappe.ui.form.on("Stock Entry",{
			after_save:function(frm,cdt,cdn){
				var data = locals[cdt][cdn]
				var doctype_name=data.doctype
				var document_name=data.name
				var expiry_date=[]
				var item_rate=[]
				var item_mrp=[]
				var item_code=[]
                for(var i=0;i<data.items.length;i++){
                    if(data.items[i].t_warehouse){
                        expiry_date.push(data.items[i].expire_dates)
                        item_rate.push(data.items[i].valuation_rates)
                        item_code.push(data.items[i].item_code)
                        item_mrp.push(data.items[i].mrp_rates)
                    }
                }
				console.log(expiry_date)
				console.log(item_rate)
				console.log(item_code,item_mrp)
				frappe.call({
					method:"sks.sks.custom.py.stock_entry.auto_batch_creations",
					args:{expiry_date,item_rate,item_code,item_mrp,doctype_name,document_name},
					callback(r){
						if(r["message"]==0){
							frm.refresh();
                            console.log("Testing")
						}
					}
				})
			}
		})
	}
})