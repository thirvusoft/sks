
frappe.ui.form.on("Employee Advance",{
	to_date:function(frm){
        var from_date = frm.doc.from_date
        var to_date = frm.doc.to_date
        var name = frm.doc.employee
	
				frappe.call({
					method:"sks.sks.custom.py.employee_advance.employee_finder",
					args:{name,from_date,to_date},
					callback(r){
				
					  
						frm.set_value( "eligible_amount" , r.message[0])
							
					}
					
                })
          
        
        

    }
})
      