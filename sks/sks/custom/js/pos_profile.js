frappe.ui.form.on("POS Profile",{
    setup:function(frm){
        frm.set_query("warehouse", function() {
            return{
                filters:[
                    ["Warehouse", "company", "in", ["", cstr(frm.doc.company)]],
                    ["Warehouse", "is_group", "=",1]
                ]
            }
        })
    }
})