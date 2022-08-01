frappe.ui.form.on("Customer",{
    onload:function(frm){
        console.log(frappe.user_roles)
        if (in_list(frappe.user_roles, "Accounts Manager")) {
            frm.set_df_property("is_credit_customer", "hidden",0);
        }
        else{
            frm.set_df_property("is_credit_customer", "hidden",1);
        }
    }
})