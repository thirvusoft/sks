frappe.ui.form.on('Delivery Note', {
    sales_order: function(frm, cdt, cdn) {
    let p= locals[cdt][cdn]
    let l=frappe.db.get_value("Sales Order", p.sales_order, ["outstanding_amount","outstanding_amount_and_total_amount"]).then(function(f){
    frappe.model.set_value(cdt,cdn, 'outstanding_amount',f.outstanding_amount)   
    frappe.model.set_value(cdt,cdn,'outstanding_amount_and_total_amount',f.message.outstanding_amount_and_total_amount)
   
    })
    
    
    }
    });
    