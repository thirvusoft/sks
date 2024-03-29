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
    setup:function(frm){
        frm.set_query('warehousebin', 'warehouse', function(frm,cdt,cdn) {
            var row = locals[cdt][cdn]
            return {
                    filters: {
                    'company':row.company
                    }
                };
            });
        frm.set_query('storebin', 'warehouse',function(frm,cdt,cdn) {
                var row = locals[cdt][cdn]
                return {
                    filters: {
                    'company':row.company
                    }
                };
            });
    }
})
