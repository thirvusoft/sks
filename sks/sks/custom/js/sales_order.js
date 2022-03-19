frappe.ui.form.on("Sales Order",{
    after_save:function(frm,cdt,cdn){
        var data=locals[cdt][cdn]
        if(cur_frm.doc.docstatus!=1){
        frappe.call({
            method:"sks.sks.custom.py.sales_order.customer_transaction_history",
            args:{
                customer:data.customer
            },
            callback: function(r){
                const d = new frappe.ui.Dialog({
                    title: "Customer transaction history",
                    static: true,
                    fields:[
                    {
                        fieldname:'table',
                        fieldtype:'HTML',
                        label:'Table'
                    },
                    {
                        fieldname:'items_add',
                        fieldtype:'MultiSelectPills',
                        label:'Select items to be added',
                        get_data: function() {
                            return r.message[2]
                        }
                    }
                    ],
                    primary_action : function(data){
                        frappe.call({
                            method:"sks.sks.custom.py.sales_order.item_append",
                            args:{item_code:data.items_add,current_document:cur_frm.doc.name},
                        callback(r){
                            frm.reload_doc();
                        }
                        })
                        d.hide()
                    }
                })
            var template = "<table><tbody>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td> {{ rows[row][col] }}</td> <td> {{ days[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table>"
            d.set_df_property('table', 'options', frappe.render(template, {rows:r.message[0], days:r.message[1]}));
            if(r.message[0].length){
                d.show();
            }
        }
        })
    }
    }
 })
 

frappe.ui.form.on("Sales Order",{
   set_warehouse:function(frm,cdt,cdn){
       var data=locals[cdt][cdn]
       frappe.call({
           method:"sks.sks.custom.py.sales_order.subwarehouse",
           args:{sub_warehouse:data.set_warehouse,company:data.company},
           callback(r){
               if(frm.fields_dict["items"].grid.get_field('item_code')) {
                   frm.set_query("item_code", "items", function() {
                       return {
                           query: "erpnext.controllers.queries.item_query",
                           filters: {'item_code' : ["in", r["message"]],'is_sales_item': 1, 'customer': cur_frm.doc.customer}
                       }
                   })
               }
           }
       })
   }
})
