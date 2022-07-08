<template>
  <v-row justify="center">
    <v-dialog v-model="closingDialog" max-width="900px">
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">{{__('Closing POS Shift')}}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12" class="pa-1">
                <template>
                  <v-data-table
                    :headers="headers"
                    :items="dialog_data.payment_reconciliation"
                    item-key="mode_of_payment"
                    class="elevation-1"
                    :items-per-page="itemsPerPage"
                    hide-default-footer
                  >
                    <template v-slot:item.closing_amount="props">
                      <v-edit-dialog
                        :return-value.sync="props.item.closing_amount"
                      >
                        {{ formtCurrency(props.item.closing_amount) }}
                        <template v-slot:input>
                          <v-text-field
                            v-model="props.item.closing_amount"
                            :rules="[max25chars]"
                            :label="frappe._('Edit')"
                            single-line
                            counter
                            type="number"
                          ></v-text-field>
                        </template>
                      </v-edit-dialog>
                    </template>
                    <template v-slot:item.difference="{ item }">{{
                      (item.difference = formtCurrency(
                         item.expected_amount - item.closing_amount
                      ))
                    }}</template>
                    <template v-slot:item.billed_amount="{ item }">{{
                      (item.billed_amount = formtCurrency(
                        item.closing_amount-item.expected_amount
                      ))
                    }}</template>
                    
                    <template v-slot:item.opening_amount="{ item }">{{
                      formtCurrency(item.opening_amount)
                    }}</template>
                    <template v-slot:item.expected_amount="{ item }">{{
                      formtCurrency(item.expected_amount)
                    }}</template>
                  </v-data-table>
                </template>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="indigo" dark @click="show_denomination">{{__('Open Denomination')}}</v-btn>
          <v-btn color="error" dark @click="close_dialog">{{__('Close')}}</v-btn>
          <v-btn color="primary" dark @click="submit_dialog">{{__('Submit')}}</v-btn>
          
          
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    closingDialog: false,
    itemsPerPage: 20,
    dialog_data: {},
    headers: [
      {
        text: __('Mode of Payment'),
        value: 'mode_of_payment',
        align: 'start',
        sortable: true,
      },
      {
        text: __('Opening Amount'),
        align: 'end',
        sortable: true,
        value: 'opening_amount',
      },
       {
        text: __('Closing Amount'),
        value: 'closing_amount',
        align: 'end',
        sortable: true,
      },
      {
        text: __('Billed Amount'),
        value: 'billed_amount',
        align: 'end',
        sortable: true,
      },
      {
        text: __('Expected Amount'),
        value: 'expected_amount',
        align: 'end',
        sortable: false,
      },
      {
        text: __('Difference'),
        value: 'difference',
        align: 'end',
        sortable: false,
      },
    ],
    max25chars: (v) => v.length <= 20 || 'Input too long!', // TODO : should validate as number
    pagination: {},
  }),
  watch: {},

  methods: {
    close_dialog() {
      this.closingDialog = false;
    },


    submit_dialog() {
      evntBus.$emit('submit_closing_pos', this.dialog_data);
      this.closingDialog = false;
    },

    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },
    show_denomination(){
      	const me = this;
		const table_fields = [
			{
				fieldname: "mode_of_payment", fieldtype: "Link",
				in_list_view: 1, label: "Mode of Payment",
				options: "Mode of Payment", reqd: 1
			},
			{
				fieldname: "opening_amount", fieldtype: "Currency",
				in_list_view: 1, label: "Opening Amount",
				options: "company:company_currency",
				change: function () {
					dialog.fields_dict.balance_details.df.data.some(d => {
						if (d.idx == this.doc.idx) {
							d.opening_amount = this.value;
							dialog.fields_dict.balance_details.grid.refresh();
							return true;
						}
					});
				}
			}
		];
		const fetch_pos_payment_methods = () => {
			const pos_profile = dialog.fields_dict.pos_profile.get_value();
			if (!pos_profile) return;
			frappe.db.get_doc("POS Profile", pos_profile).then(({ payments }) => {
				dialog.fields_dict.balance_details.df.data = [];
				payments.forEach(pay => {
					const { mode_of_payment } = pay;
					dialog.fields_dict.balance_details.df.data.push({ mode_of_payment, opening_amount: '0' });
				});
				dialog.fields_dict.balance_details.grid.refresh();
			});
		}
		const dialog = new frappe.ui.Dialog({
			title: __('Create POS Opening Entry'),
			// static: true,
			fields: [
				{
					fieldtype: 'Link', label: __('Company'), default: frappe.defaults.get_default('company'),
					options: 'Company', fieldname: 'company', reqd: 1
				},
				{
					fieldtype: 'Link', label: __('POS Profile'),
					options: 'POS Profile', fieldname: 'pos_profile', reqd: 1,
					get_query: () => pos_profile_query,
					onchange: () => fetch_pos_payment_methods()
				},
				{
					fieldname: "balance_details",
					fieldtype: "Table",
					label: "Opening Balance Details",
					cannot_add_rows: false,
					in_place_edit: true,
					reqd: 1,
					data: [],
					fields: table_fields
				}
			],
			primary_action: async function({ company, pos_profile, balance_details }) {
				if (!balance_details.length) {
					frappe.show_alert({
						message: __("Please add Mode of payments and opening balance details."),
						indicator: 'red'
					})
					return frappe.utils.play_sound("error");
				}

				// filter balance details for empty rows
				balance_details = balance_details.filter(d => d.mode_of_payment);

				const method = "erpnext.selling.page.point_of_sale.point_of_sale.create_opening_voucher";
				const res = await frappe.call({ method, args: { pos_profile, company, balance_details }, freeze:true });
				!res.exc && me.prepare_app_defaults(res.message);
				dialog.hide();
			},
			primary_action_label: __('Submit')
		});
		dialog.show();
		const pos_profile_query = {
			query: 'erpnext.accounts.doctype.pos_profile.pos_profile.pos_profile_query',
			filters: { company: dialog.fields_dict.company.get_value() }
		}

                        


      // evntBus.$emit('set_customer', 'aaaa');


       
            // frappe.call({
            //   method:"posawesome.posawesome.api.posapp.get_fields_for_denomination",
            //   callback(r){
            //       console.log(r.message)
            //  var d = new frappe.ui.Dialog({
            //     title: "Denomination",
            //     fields:[
            //       {'fieldname':'table','fieldtype':'Data','label':"kkk",'default':"lkkkkk",'in_place_edit':1},
            //       {'fieldname':'table','fieldtype':'Data','options':"r.message"}
            //     ],
            //     primary_action_label:"Close",
            //     primary_action: function(data){
            //       console.log(data)
            //       d.hide()
            //     }
            //   });

            //   d.show()
            
            //    }
            // })
    }
    
  },
  created: function () {
    evntBus.$on('open_ClosingDialog', (data) => {
      this.closingDialog = true;
      this.dialog_data = data;
    });
  },
};
</script>
