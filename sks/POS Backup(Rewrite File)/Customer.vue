<template>
  <div>
    
    <v-autocomplete
      dense
      clearable
      auto-select-first
      outlined
      color="indigo"
      :label="frappe._('Customer')"
      v-model="customer"
      :items="customers"
      item-text="customer_name"
      item-value="name"
      background-color="white"
      :no-data-text="__('Customer not found')"
      hide-details
      :filter="customFilter"
      :disabled="readonly"
      append-icon="mdi-account-plus"
      @click:append="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
    >
      <template v-slot:item="data">
        <template>
          <v-list-item-content>
            <v-list-item-title
              class="indigo--text subtitle-1"
              v-html="data.item.customer_name"
            ></v-list-item-title>
            <v-list-item-subtitle
              v-if="data.item.customer_name != data.item.name"
              v-html="`ID: ${data.item.name}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.tax_id"
              v-html="`TAX ID: ${data.item.tax_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.email_id"
              v-html="`Email: ${data.item.email_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.mobile_no"
              v-html="`Mobile No: ${data.item.mobile_no}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.primary_address"
              v-html="`Primary Address: ${data.item.primary_address}`"
            ></v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </template>
    </v-autocomplete>
  </div>
  
</template>



<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
  }),

  methods: {
    get_customer_names() {
      const vm = this;
      if (vm.pos_profile.posa_local_storage && localStorage.customer_storage) {
        vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
      }
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_names',
        args: {
          pos_profile: this.pos_profile.pos_profile,
        },
        callback: function (r) {
          if (r.message) {
            vm.customers = r.message;
            console.info('loadCustomers');
            if (vm.pos_profile.posa_local_storage) {
              localStorage.setItem('customer_storage', '');
              localStorage.setItem(
                'customer_storage',
                JSON.stringify(r.message)
              );
            }
          }
        },
      });
    },
    new_customer() {
      evntBus.$emit('open_new_customer');
    },
    edit_customer() {
      evntBus.$emit('open_edit_customer');
    },
 
  
    customFilter(item, queryText, itemText) {
      const textOne = item.customer_name
        ? item.customer_name.toLowerCase()
        : '';
      const textTwo = item.tax_id ? item.tax_id.toLowerCase() : '';
      const textThree = item.email_id ? item.email_id.toLowerCase() : '';
      const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : '';
      const textFifth = item.name.toLowerCase();
      const searchText = queryText.toLowerCase();

      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1
      );
    },
  },

  computed: {},

// CREATE
   created: function () {
    this.customer = customer;
    var vm = this;
    var customer = vm.customer;
    var _h = vm.$createElement;
    var _c = vm._self._c || _h;
    var  credit_limit;
    
    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.$on('set_customer', (customer) => {
        this.customer = customer;
        

      //.....................................................

        customer =vm.customer;
         if(customer){

          frappe.db.get_value("Customer",customer,'payment_terms').then(function(value){
            credit_limit = value.message.payment_terms
          })

        frappe.call({
          method : "posawesome.posawesome.api.credit_sales.customer_credit_sale",
          args:{
            customer: customer
          },
          callback : function(r){
            if(r.message[0]>0){
              let modes=[];
              for(var i=0; i<vm.pos_profile.pos_profile.payments.length; i++){
                modes.push(vm.pos_profile.pos_profile.payments[i].mode_of_payment)
              }
            var d = new frappe.ui.Dialog({
              size: "large",
              title:"Customer: "+ customer +"'s Outstanding Amount",
              fields:[
                {fieldname:'items', fieldtype:'Table', fields:[
                {
                  label: 'Sales Invoice No',
                  fieldname: 'sales_invoice',
                  fieldtype: 'Read Only',
                  options: 'Sales Invoice',
                  in_list_view:1,
                  columns:3
                },
                {
                  label: 'Outstanding Amount',
                  fieldname: 'amount',
                  fieldtype: 'Read Only',
                  in_list_view:1,
                  columns:3
                },
                {
                  label: 'Paying Amount',
                  fieldname: 'paid',
                  fieldtype: 'Float',
                  in_list_view:1,
                  columns:2
                },
                 {
                  label: 'Mode of Payment',
                  fieldname: 'mode_of_payment',
                  fieldtype: 'Select',
                  options:modes,
                  in_list_view:1,
                  columns:2
                }
                ],
                data:r.message[1]},
                {'label':'Outstanding Amount','fieldname':'outstanding','fieldtype':'Currency','default':r.message[0],'read_only':1},
                {'label':'Reference Number','fieldname':'ref_no','fieldtype':'Data', 'depends_on':'eval:doc.mode=="Credit Card"'},
                {'label':'Reference Date','fieldname':'ref_date','fieldtype':'Date', 'default':'Today','depends_on':'eval:doc.mode=="Credit Card"'}
              ],
              primary_action : function(data){
                console.log(data)
                frappe.call(
                  'posawesome.posawesome.api.posapp.check_opening_shift', 
                  {user: frappe.session.user,}).then(function (id) {
                    if (r.message && data.items) {
                      frappe.call({
                        method:"posawesome.posawesome.api.credit_sales.payment_entry",
                        args:{
                          customer:customer,
                          pending_invoice:data.items,
                          company:vm._data.pos_profile.company.company_name,
                          opening : id.message.pos_opening_shift.name,
                          ref_no: data.ref_no,
                          ref_date: data.ref_date
                          
                        },
                        callback : function(res){
                            if(res.message){
                              evntBus.$emit('show_mesage', {
                                text: __(`${res.message} Payment Entries Created Successfully.`),
                                color: 'success',
                              });

                            }
                        }
                      });
                    }
                  });

                
                d.hide();
              }
            });
            d.show();
          }
        }
        });
        }
      });
      evntBus.$on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      evntBus.$on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
    });
  },

  watch: {
    customer() {
      evntBus.$emit('update_customer', this.customer);
    },
   
  },
};
</script>
