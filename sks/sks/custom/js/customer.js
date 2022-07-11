frappe.ui.form.on("Customer",{
    onload:function(frm){
        if (frm.doc.__islocal && in_list(frappe.user_roles, "Accounts Manager")) {
            frm.set_df_property("is_credit_customer", "hidden",0);
        }
        else{
            frm.set_df_property("is_credit_customer", "hidden",1);
        }
    }
})