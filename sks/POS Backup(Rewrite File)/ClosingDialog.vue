<template>
  <v-row justify="center">
    <v-dialog v-model="closingDialog" max-width="900px">
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">{{__('THIRVU RETAIL Closing Shift')}}</span>
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
                         -(item.expected_amount - item.closing_amount)
                      ))
                    }}</template>
                    <template v-slot:item.billed_amount="{ item }">{{
                      (item.billed_amount = formtCurrency(
                        -(item.closing_amount-item.expected_amount)
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

// Customized By Thirvusoft
// Start
    submit_dialog() {
      // evntBus.$emit('submit_closing_pos', this.dialog_data);
      // this.closingDialog = false;
    },
// End
    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },
 
    
  },

  created: function () {
    // Customized By Thirvusoft
    // Start
    evntBus.$on('open_ClosingDialog', (data) => {
      var pos_opening_shift=data.pos_opening_shift
      frappe.call({
        method:"posawesome.posawesome.api.posapp.get_fields_for_denomination",
        args:{pos_opening_shift},
        callback(r){
          var d = new frappe.ui.Dialog({
            title: "Thirvu Closing Shift",
            fields:[{
              
              label:"Denomination",fieldname:"ts_denomination",fieldtype:"Table",cannot_add_rows: 1,in_place_edit: true,ts_block:"Yes",fields:[
                {
                  label: 'Amount',
                  fieldname: 'ts_amount',
                  fieldtype: 'Read Only',
                  in_list_view:1,
                  columns:1,
					      },
                {
                  label: 'Count',
                  fieldname: 'ts_count',
                  fieldtype: 'Int',
                  default:0,
                  in_list_view:1,
                  columns:1,
					      },
              ],data:r.message[0],
            },
              {label:"Mode of Payments",fieldname:"ts_mode_of_payment",fieldtype:"Table",cannot_add_rows:1,in_place_edit: true,ts_block:"Yes",fields:[
                {
                  label: 'Type',
                  fieldname: 'ts_type',
                  fieldtype: 'Read Only',
                  in_list_view:1,
                  columns:1,
					      },
                {
                  label: 'Amount',
                  fieldname: 'ts_amount',
                  fieldtype: 'Currency',
                  in_list_view:1,
                  columns:1,
					      },
              ],data:r.message[1]
              }],
            primary_action_label:"Submit",
            primary_action: function(ts_denomination){
              data["ts_denomination"]=ts_denomination
              this.closingDialog = true;
              this.dialog_data = data;
              evntBus.$emit('submit_closing_pos', this.dialog_data);
              this.closingDialog = false;
              d.hide()
              frappe.show_alert({ message: __("Thirvu Closing Shift Created Successfully"), indicator: 'green' });
              location.href='/app/home';  
            }
          });
        d.show()
        }
      })
    });
    // End
  },
};
</script>
