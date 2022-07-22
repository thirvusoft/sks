// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
	
frappe.ui.form.on("Employee Bonus Tool",{
	department:function(frm,cdt,cdn){
		var bonus=locals[cdt][cdn]
		var from_date=frm.doc.from_date
		var to_date = frm.doc.to_date
		var bonus1=bonus.department
		if(!from_date || !to_date){
			frappe.throw("Please Select From Date And To Date")
		}
		else{
			frappe.call({
		
				method:"sks.sks.doctype.employee_bonus_tool.employee_bonus_tool.employee_finder",
				args:{bonus1,from_date,to_date},
				callback(r){
					var total =0
					frm.trigger("from_date")
					frm.trigger("to_date")
					frm.clear_table("employee_bonus_details");
					for(var i=0;i<r.message[0].length;i++){
						var child = cur_frm.add_child("employee_bonus_details");
				        total += r.message[1][i]
						frappe.model.set_value(child.doctype, child.name, "employee", r.message[0][i]["name"])
						frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[0][i]["employee_name"])
						frappe.model.set_value(child.doctype, child.name, "department", bonus1)
						frappe.model.set_value(child.doctype, child.name, "current_bonus", r.message[1][i])
					}
					cur_frm.set_value("total_bonus_amount",total)
					cur_frm.refresh_field("employee_bonus_details")
				}
				
			})
		
		
		}
	},
	
	on_submit:function(frm,cdt,cdn){
		var bonus=locals[cdt][cdn]
		for(var i=0;i<bonus.employee_bonus_details.length;i++){
			frappe.call({
				method:"sks.sks.doctype.employee_bonus_tool.employee_bonus_tool.create_bonus",
				args:{amount:bonus.employee_bonus_details[i].current_bonus,
					name:bonus.employee_bonus_details[i].employee,
					date:frm.doc.date,
					doc:frm.doc.name},
			})
		}
	},
	
	
});
	 
