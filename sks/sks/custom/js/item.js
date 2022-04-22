frappe.ui.form.on("Item",{
    onload:function(frm){
        frm.set_value("has_batch_no",1)
        frm.set_value("create_new_batch",1)
        frm.set_value("batch_number_series",".{item}.-.YY.MM.-")
    },
})