frappe.ui.form.on("Job Offer",{
    designation:function(frm){
        if(frm.doc.designation){
            frm.clear_table('offer_terms');
            frappe.db.exists('Job Offer Template', frm.doc.designation).then(exists => {
                if(exists){
                    frappe.model.with_doc('Job Offer Template', frm.doc.designation, function () {
                        let source_doc = frappe.model.get_doc('Job Offer Template', frm.doc.designation);
                        $.each(source_doc.job_template, function (index, source_row) {
                            const target_row = frm.add_child('offer_terms');
                            target_row.offer_term = source_row.offer_term;
                            target_row.value = source_row.value;
                            frm.refresh_field('offer_terms');
                        });
                    });
                }
                else{
                    frappe.msgprint(__("Template is not assigned for {0}", [frm.doc.designation]));
                }
            });  
        }
        else{
            frm.clear_table('offer_terms')
            frm.refresh_field('offer_terms');
        }
    },
})