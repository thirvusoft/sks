frappe.ui.form.on('Employee',{
    gender:function(frm){
        if(frm.doc.__islocal){
            frappe.db.get_doc("Thirvu HR Settings")
            .then((doc) => {
                    if(doc.company_property.length){
                    frm.clear_table('ts_property_details')
                    for (let data in doc.company_property){
                        frappe.db.get_value("Thirvu Property", {"name": doc.company_property[data].property_name}, "category", (r) => {
                            if(r.category == frm.doc.gender){
                                let row = frm.add_child("ts_property_details");
                                row.property = doc.company_property[data].property_name;
                                row.amount = doc.company_property[data].amount
                                frm.refresh_field("ts_property_details");
                            }
                            else if(r.category == 'Both'){
                                let row = frm.add_child("ts_property_details");
                                row.property = doc.company_property[data].property_name;
                                row.amount = doc.company_property[data].amount
                                frm.refresh_field("ts_property_details");
                            }
                        });
                    }
                }
                else{
                    frappe.msgprint('Kindly Enter the Property Details in Thirvu HR Settings')
                }
            })
        }
    },
    validate:function(frm){
        if(frm.doc.relieving_date){
            var d = new Date(frm.doc.date_of_joining);
            var year = d.getFullYear();
            var month = d.getMonth();
            var day = d.getDate();
            var one_year_date = new Date(year + 1, month, day);
            if(new Date(frm.doc.relieving_date) <= one_year_date){
                frappe.call({
                    method:"sks.sks.custom.py.employee.property_deduction",
                    args:{doc:frm.doc}
                })  
            } 
        }       
    },
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
