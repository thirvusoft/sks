var ts_company=""
frappe.ui.form.on("POS Profile",{
    setup:function(frm){
        ts_company=frm.doc.company
        frm.set_query("warehouse", function() {
            return{
                filters:[
                    ["Warehouse", "company", "in", ["", cstr(frm.doc.company)]],
                    ["Warehouse", "is_group", "=",1]
                ]
            }
        })
        // frm.set_query('item_name', 'ts_closing_stock_details_table', function() {
        //     return{
        //         filters: {
        //         'is_closing_shift_stock':1
        //         }
        //     };
        // });
    }
})

frappe.ui.form.on("Thirvu Closing Shift Stock Details",{
    item_name:function(frm,cdt,cdn){
        var ts_data=locals[cdt][cdn]
        var item_name=ts_data.item_name
        if(item_name && ts_company){
            frappe.call({
                method:"sks.sks.custom.py.pos_profile.item_warehouse_fetching",
                args:{item_name,ts_company},
                callback(r){
                    if(r.message){
                        frappe.model.set_value(ts_data.doctype, ts_data.name, "bin", r.message)   
                    }
                    else{
                        frappe.show_alert({ message: __('There Is No Store Bin for Item '+item_name), indicator: 'red' });
                    }
                }
            })  
        }
    }
})