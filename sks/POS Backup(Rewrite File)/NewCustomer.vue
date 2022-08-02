<template>
  <v-row justify="center">
    <v-dialog v-model="customerDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">{{ __('New Customer') }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Customer Name')"
                  background-color="white"
                  hide-details
                  v-model="customer_name"
                  ref="cus"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Mobile')"
                  background-color="white"
                  hide-details
                  v-model="mobile1"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Address Line')"
                  background-color="white"
                  hide-details
                  v-model="address1"
                ></v-text-field>
              </v-col>
              <!-- <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Address Line2')"
                  background-color="white"
                  hide-details
                  v-model="address2"
                ></v-text-field>
              </v-col> -->
               <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="indigo"
                  :label="frappe._('Area')"
                  v-model="territory"
                  :items="territorys"
                  background-color="white"
                  :no-data-text="__('Territory not found')"
                  hide-details
                >
                </v-autocomplete>
              </v-col>
              <!-- <v-col cols="6">
                <v-autocomplete
                 clearable
                  dense
                  auto-select-first
                  color="indigo"
                  :label="frappe._('City*')"
                  v-model="city"
                  :items="citys"
                  background-color="white"
                  :no-data-text="__('City not found')"
                  hide-details
                ></v-autocomplete>
              </v-col> -->
           
              <!-- <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="indigo"
                  :label="frappe._('Customer Group*')"
                  v-model="group"
                  :items="groups"
                  background-color="white"
                  :no-data-text="__('Group not found')"
                  hide-details
                >
                </v-autocomplete>
              </v-col> -->
             
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">{{
            __('Close')
          }}</v-btn>
          <v-btn color="primary" dark @click="submit_dialog">{{
            __('Submit')
          }}</v-btn>
        </v-card-actions>
        </v-card>
      
    </v-dialog>
    
  </v-row>
  
</template>


<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    customerDialog: false,
    pos_profile: '',
    customer_name: '',
    mobile1: '',
    address1: '',
    address2:'',
    city:'',
    c_group:'',
    group: '',
    groups: '',
    territory: '',
    territorys: '',
  }),
  watch: {},
  methods: {
   
    close_dialog() {
      this.customerDialog = false;
    },
    getCustomerGroups() {
      if (this.groups.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Customer Group', {
          fields: ['name'],
          page_length: 1000,
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.groups.push(el.name);
            });
          }
        });
    },
    getCustomerTerritorys() {
      if (this.territorys.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Territory', {
          fields: ['name'],
          page_length: 1000,
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.territorys.push(el.name);
            });
          }
        });
    },
    
    
    submit_dialog() {
      
      if (this.customer_name) {
        const args = {
          customer_name: this.customer_name,
          mobile1: this.mobile1,
          address1: this.address1,
          address2:this.address2?this.address2:'',
          area:this.territory,
          city: this.city,
          c_group:this.group,

        };
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.create_customer',
          args: args,
          callback: (r) => {
            if (!r.exc && r.message.name) {
              evntBus.$emit('show_mesage', {
                text: __('Customer contact created successfully.'),
                color: 'success',
              });
              args.name = r.message.name;
              frappe.utils.play_sound('submit');
              evntBus.$emit('add_customer_to_list', args);
              evntBus.$emit('set_customer', r.message.name);
              this.customer_name='',
              this.mobile1=''
              this.address1=''
              this.address2=''
              this.territory=''
              this.city=''
              this.group=''
              this.customerDialog = false;
            }
          },
        });
        
      }
      
    },
    
  },


    
  
  
  created: function () {
    evntBus.$on('open_new_customer', () => {
      this.customerDialog = true;
      var  groups, territorys, citys;
      // v_model;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.customer_link_details",
        async: false,
        callback(r){
        groups = r.message[0]
        territorys= r.message[1]
        citys= r.message[2]
          }
      })
      this.groups = groups
      this.territorys = territorys
      this.citys= citys
      
      
    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    
    // this.getCustomerGroups();
    // this.getCustomerTerritorys();
  },
  
  
  data: () => ({
    customerDialog: false,
    pos_profile: '',
    customer: '',
  }),
  watch: {},
};

 

</script>



