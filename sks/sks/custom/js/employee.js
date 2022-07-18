frappe.ui.form.on("Employee",{
	date_of_birth:function(frm){
        var date_of_birth = frm.doc.date_of_birth
        frappe.call({
            method:"sks.sks.custom.py.employee.age_calculation",
            args:{date_of_birth},
            callback(y){
        
             
                frm.set_value( "age" , y.message)
                    
            }
            
        })
    }
})
