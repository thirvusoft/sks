frappe.ui.form.on('Delivery Note', {
    sales_order: function(frm, cdt, cdn) {
    let outstanding_amount= locals[cdt][cdn]
    let outstanding_amount_and_total_amount=frappe.db.get_value("Sales Order", outstanding_amount.sales_order, ["outstanding_amount","outstanding_amount_and_total_amount"]).then(function(f){
    frappe.model.set_value(cdt,cdn, 'outstanding_amount',f.outstanding_amount)   
    frappe.model.set_value(cdt,cdn,'outstanding_amount_and_total_amount',f.message.outstanding_amount_and_total_amount)
   
    })
    
    
    }
    });
    
