frappe.ui.form.on("Item",{
    onload:function(frm){
        if(cur_frm.is_new()){
            frappe.db.get_single_value("Thirvu Retail Settings","automatic_batch_creation").then(value =>{
                if(value==1){
                    frm.set_value("has_batch_no",1)
                }
            })
            frm.set_value("create_new_batch",1)
            frm.set_value("batch_number_series",".{item}.-.YY.MM.-")
        }
    },
})


frappe.ui.form.on("Item Warehouse",{
    company: function(frm,cdt,cdn) {
        var row = locals[cdt][cdn]
        frm.set_query('warehousebin', 'warehouse', function() {

        return {
        filters: {
        'company':row.company
        }
        };
        });
   },
})

frappe.ui.form.on("Item Warehouse",{
    company: function(frm,cdt,cdn) {
        var row = locals[cdt][cdn]
        frm.set_query('storebin', 'warehouse', function() {

        return {
        filters: {
        'company':row.company
        }
        };
        });
   },
})