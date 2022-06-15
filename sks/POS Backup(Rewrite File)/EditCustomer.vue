<template>
  <v-row justify="center">
    <v-dialog v-model="customerDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">{{ __('Customer Info') }}</span>
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
                  readonly
                  v-model="customer_info.customer_name"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Mobile No1')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.mobile_no"
                  @change="set_customer_info('mobile_no', $event)"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Address Line1')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.address_line1"
                  @change="set_customer_info('address_line1', $event)"
                ></v-text-field>
              </v-col>
               <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Address Line2')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.address_line2"
                  @change="set_customer_info('address_line2', $event)"
                ></v-text-field>
              </v-col> <v-col cols="6">
                <v-autocomplete
                  dense
                  color="indigo"
                  :label="frappe._('Area')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.territory"
                  :items="territorys"
                  @change="set_customer_info('territory', $event)"
                ></v-autocomplete>
              </v-col> <v-col cols="6">
                <v-autocomplete
                  dense
                  color="indigo"
                  :label="frappe._('City')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.city"
                  :items="citys"
                  @change="set_customer_info('city', $event)"
                ></v-autocomplete>
              </v-col>
               <v-col cols="6">
                <v-autocomplete
                  dense
                  color="indigo"
                  :label="frappe._('Customer Group')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.customer_group"
                  :items="groups"
                  @change="set_customer_info('customer_group', $event)"
                ></v-autocomplete>
              </v-col>

              
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

     <v-dialog v-model="vehicleDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline indigo--text">{{ __('Vehicle Info') }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Vehicle Name')"
                  background-color="white"
                  hide-details
                  readonly
                  v-model="vehicle_info.name"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  dense
                  color="indigo"
                  :label="frappe._('Vehicle Category')"
                  v-model="vehicle_info.vehicle_category"
                  :items = "v_category"
                  background-color="white"
                  hide-details
                  @change="set_vehicle_info('vehicle_category', $event)"
                ></v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  dense
                  color="indigo"
                  :label="frappe._('Vehicle Model')"
                  :items = "v_model"
                  background-color="white"
                  hide-details
                  v-model="vehicle_info.ts_vehicle_model"
                  @change="set_vehicle_info('ts_vehicle_model', $event)"
                ></v-autocomplete>
              </v-col>
               <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Vehicle Year')"
                  background-color="white"
                  hide-details
                  v-model="vehicle_info.vehicle_year"
                  @change="set_vehicle_info('vehicle_year', $event)"
                ></v-text-field>
              </v-col>
               <v-col cols="6">
                <v-text-field
                  dense
                  color="indigo"
                  :label="frappe._('Vehicle No')"
                  background-color="white"
                  v-model="vehicle_info.ts_vehicle_no"
                  @change="set_vehicle_info('ts_vehicle_no', $event)"
                ></v-text-field>
              </v-col>
             
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close__vehicle_dialog">Close</v-btn>
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
    customer_info: '',
    vehicleDialog: false,
    vehicle_info:'',
    v_category: '',
    v_model: '',
    territorys:'',
    citys:'',
    groups:''

  }),

  // watch: {
  //   customer() {
  //     this.fetch_customer_details();
  //   },
  // },

  methods: {
    close_dialog() {
      this.customerDialog = false;
    },
     close__vehicle_dialog() {
      this.vehicleDialog = false;
    },
    set_customer_info(field, value) {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.set_customer_info',
        args: {
          fieldname: field,
          customer: this.customer_info.name,
          value: value,
        },
        callback: (r) => {
          if (!r.exc) {
            vm.customer_info[field] = value;
            evntBus.$emit('show_mesage', {
              text: __('Customer contact edited successfully.'),
              color: 'success',
            });
            frappe.utils.play_sound('submit');
          }
        },
      });
    },
    set_vehicle_info(){
      const vm = this;
      if(this.vehicle_info.vehicle_year){
      frappe.call({
         method: "posawesome.posawesome.api.posapp.update_vehicle",
              args:{
                data: this.vehicle_info,
                },
              callback(r){
                
     
                evntBus.$emit('show_mesage', {
                  text: __('Vehicle Edited successfully'),
                  color: 'success',
                });
                 
              }   
      })
       this.vehicleDialog = false;

    }
     setTimeout(()=>{window.location.reload();}, 2000);
    }
    
  },



  created: function () {
     evntBus.$on('update_vehicle',  (vehicle,customer) => {
        this.vehicle = vehicle
        var vehicle_info;
          if(this.vehicle){
        frappe.call({
        method: "posawesome.posawesome.api.posapp.get_vehicle_info",
        args:{
          customer:customer,
          vehicle:this.vehicle,
          },
        async: false,
        callback(r){
         vehicle_info = r.message
          }
      })

      this.vehicle_info = vehicle_info[0]
      }
      });


    evntBus.$on('open_edit_vehicle', () => {
      this.vehicleDialog = true;
      var  v_category, v_model;
      frappe.call({
        method: "posawesome.posawesome.api.posapp.vehicle_link_details",
        async: false,
        callback(r){
         v_category = r.message[1]
         v_model = r.message[0]
          }
      })
      this.v_category = v_category
      this.v_model = v_model
    });
    
    evntBus.$on('open_edit_customer', () => {
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


    evntBus.$on('set_customer_info_to_edit', (data) => {
      this.customer_info = data;
    });


     evntBus.$on('set_vehicle_info_to_edit', (data) => {
      this.vehicle_info = data;
    });



  },
};
</script>


