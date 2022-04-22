frappe.ui.form.on("Item",{
    onload:function(frm){
        frm.set_value("has_batch_no",1)
        frm.set_value("create_new_batch",1)
        frm.set_value("batch_number_series",".{item}.-.YY.MM.-")
    },
    validate:function(frm,cdt,cdn){
        var validate=0
        var data=locals[cdt][cdn]
        if(data.ts_is_markdown==1){
            validate=validate+1
        }
        if(data.ts_is_markup==1){
            validate=validate+1
        }
        if(validate==0){
            frappe.throw({
                title:("Message"),
                message:("Please Select Markup Price or Markdown Price")
            })
        }
    }
})