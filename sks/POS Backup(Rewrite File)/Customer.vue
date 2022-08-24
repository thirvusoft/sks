
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
      :loading="isLoading"
      :items="fetchcustomers"
      :search-input.sync="search"
      item-text="customer_name"
      item-value="name"
      ref = "customer"
      hide-selected
      background-color="white"
      :no-data-text="__('Create New Customer')"
      :filter="customFilter"
      :disabled="readonly"
      append-icon="mdi-account-plus"
      @click:append="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
      return-object
    >
      <template v-slot:item="data">
        <template>
          <v-list-item-content>
            <v-list-item-title
              class="indigo--text subtitle-1"
              v-html="data.item.customer_name"
            ></v-list-item-title>
            <!-- Customized By Thirvusoft
            Start -->
            <!-- <v-list-item-subtitle
              v-if="data.item.customer_name != data.item.name"
              v-html="`ID: ${data.item.name}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.tax_id"
              v-html="`TAX ID: ${data.item.tax_id}`"
            ></v-list-item-subtitle> -->
            <!-- <v-list-item-subtitle
              v-if="data.item.email_id"
              v-html="`Email: ${data.item.email_id}`"
            ></v-list-item-subtitle> -->
            <v-list-item-subtitle
              v-if="data.item.mobile_no"
              v-html="`Mobile No: ${data.item.mobile_no}`"
            ></v-list-item-subtitle>
            <!-- <v-list-item-subtitle
              v-if="data.item.primary_address"
              v-html="`Primary Address: ${data.item.primary_address}`"
            ></v-list-item-subtitle> -->
            <!-- End -->
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
    pagelength :10,
    customers: [],
    // Customized By Thirvusoft
    // Start
    a:"",
    // End
    readonly: false,
    isLoading: false,
    customer: '',
    search: null
  }),

  computed: {
    fields () {
      if (!this.customer) return []

      return Object.keys(this.customer).map(key => {
        return {
          key,
          value: this.customer[key] || 'n/a'
        }
      })
    },
    fetchcustomers () {
      return this.customers.map(entry => {
        return Object.assign({}, entry)
      })
    }
  },
  

  watch: {
    search (val) {
      if (!val) {
        return
      }

      this.clearEntries()
      this.isLoading = true
      this.fetchEntriesDebounced(val)
    }
  },

  methods: {
    clearEntries() {
      this.count = 0
      this.customers = []
    },
    fetchEntriesDebounced(val) {
      clearTimeout(this._searchTimerId)
      this._searchTimerId = setTimeout(() => {
        this.fetchEntries(val)
      }, 500) /* 500ms throttle */
    },
    fetchEntries(val) {
      frappe.call('posawesome.posawesome.api.posapp.get_customer_names', {
					searchterm: val
				})
				.then(r => {
					this.count = r.message[1]
          this.customers = r.message[0]
				})
				.then(() => (this.isLoading = false));
    },
    get_customer_names() {
      // const vm = this;
      
      // if (vm.pos_profile.posa_local_storage && localStorage.customer_storage) {
      //   vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
      // }
      // frappe.call({
      //   method: 'posawesome.posawesome.api.posapp.get_customer_names',
      //   args: {
      //     pos_profile: this.pos_profile.pos_profile,
      //   },
      //   callback: function (r) {
      //     if (r.message) {
      //       vm.customers = r.message;
            
      //       console.info('loadCustomers');
      //       console.info('testCustomers');
      //       if (vm.pos_profile.posa_local_storage) {
      //         localStorage.setItem('customer_storage', '');
      //         localStorage.setItem(
      //           'customer_storage',
      //           JSON.stringify(r.message)
      //         );
      //       }
      //     }
      //   },
      // });
    },
    new_customer() {
    // Customized By Thirvusoft
    // Start
      evntBus.$emit('open_new_customer',a);
    // End
    },
    edit_customer() {
      evntBus.$emit('open_edit_customer');
    },
    // Customized By Thirvusoft
    // Start
    shortOpenNewCustomer: function shortOpenNewCustomer(e) {
        if (e.key === 'F3') {
          e.preventDefault();
          this.new_customer();
        }
      },
      shortOpenEditCustomer: function shortOpenEditCustomer(e) {
        if (e.key === 'F4') {
          e.preventDefault();
          this.edit_customer();
        }
      },
      shortOpenCustomer: function shortOpenCustomer(e) {
        if (e.key === 'F2') {
          e.preventDefault();
          this.$refs.customer.focus();
        }
      },
    // End
    customFilter(item, queryText, itemText) {
      
      const textOne = item.customer_name
        ? item.customer_name.toLowerCase()
        : '';
      const textTwo = item.tax_id ? item.tax_id.toLowerCase() : '';
      const textThree = item.email_id ? item.email_id.toLowerCase() : '';
      const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : '';
      const textFifth = item.name.toLowerCase();
      const searchText = queryText.toLowerCase();
      a=queryText
      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1
      );
    },
  },

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
        

      // Customized By Thirvusoft
      // Start
      frappe.db.get_single_value("Thirvu Retail Settings","allow_display_customer_outstanding_amount").then(value =>{
	      if(value==1){
        customer =vm.customer.name;
         if(customer){

          frappe.db.get_value("Customer",customer,'payment_terms').then(function(value){
            credit_limit = value.message.payment_terms
          })

        frappe.call({
          method : "posawesome.posawesome.api.posapp.customer_credit_sale",
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
                {fieldname:'items', fieldtype:'Table', cannot_add_rows: 1,in_place_edit: true,ts_block:"Yes",fields:[
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
                  columns:2,
                  onchange: async function(){
                    let items=d.get_value('items')
                    let bank=false
                    for(let mop=0; mop<items.length; mop++){
                      let mode = items[mop].mode_of_payment
                      if(mode){
                        await frappe.db.get_value('Mode of Payment', mode, 'type').then((res) =>{
                          if(res.message.type=='Bank'){
                            bank=true
                            d.set_df_property('ref_no', 'hidden', 0)
                            d.set_df_property('ref_no', 'reqd', 1)
                            d.set_df_property('ref_date', 'hidden', 0)
                            d.set_df_property('ref_date', 'reqd', 1)
                          }
                          else{
                            d.set_df_property('ref_no', 'hidden', 1)
                            d.set_df_property('ref_no', 'reqd', 0)
                            d.set_df_property('ref_date', 'hidden', 1)
                            d.set_df_property('ref_date', 'reqd', 0)
                          }
                        })
                      }
                    }
                  }
                }
                ],
                data:r.message[1]},
                {'label':'Outstanding Amount','fieldname':'outstanding','fieldtype':'Currency','default':r.message[0],'read_only':1},
                {'label':'Reference Number','fieldname':'ref_no','fieldtype':'Data', 'hidden':1, default: 'Nothing'},
                {'label':'Reference Date','fieldname':'ref_date','fieldtype':'Date', 'default':'Today', 'hidden':1}
              ],
              primary_action : function(data){
                frappe.call(
                  'posawesome.posawesome.api.posapp.check_opening_shift', 
                  {user: frappe.session.user,}).then(function (id) {
                    if (r.message && data.items) {
                      frappe.call({
                        method:"posawesome.posawesome.api.posapp.payment_entry",
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
        }
        })
      });
      // End
      evntBus.$on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      evntBus.$on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
    });
    // Customized By Thirvusoft
    // Start
    document.addEventListener('keydown', this.shortOpenNewCustomer.bind(this));
    document.addEventListener('keydown', this.shortOpenEditCustomer.bind(this));
    document.addEventListener('keydown', this.shortOpenCustomer.bind(this));
  },
  destroyed: function destroyed() {
    document.removeEventListener('keydown', this.shortOpenNewCustomer);
    document.removeEventListener('keydown', this.shortOpenEditCustomer);
    document.removeEventListener('keydown', this.shortOpenCustomer);
  },
  // End
  watch: {
     search (val) {
      if (!val) {
        return
      }

      this.clearEntries()
      this.isLoading = true
      this.fetchEntriesDebounced(val)
    },
    customer() {
      evntBus.$emit('update_customer', this.customer);
    },
   
  },
};
</script>
