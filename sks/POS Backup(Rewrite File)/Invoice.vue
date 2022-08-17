
<template>
  <div>
    <v-dialog v-model="cancel_dialog" max-width="330">
      <v-card>
        <v-card-title class="text-h5">
          {{ __('Cancel Current Invoice ?') }}
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="cancel_invoice">
            {{ __('Cancel') }}
          </v-btn>
          <v-btn color="primary" @click="cancel_dialog = false">
            {{ __('Back') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-card
      style="max-height: 82vh; height: 82vh"
      class="cards my-0 py-0 grey lighten-5"
    >
      <v-row align="center" class="items px-2 py-1">
        <v-col
          v-if="pos_profile.posa_allow_sales_order"
          cols="9"
          class="pb-0 mb-2 pr-0"
        >
          <Customer></Customer>
        </v-col>
        <v-col
          v-if="!pos_profile.posa_allow_sales_order"
          cols="12"
          class="pb-0 mb-2"
        >
          <Customer></Customer>
        </v-col>
        <v-col
          v-if="pos_profile.posa_allow_sales_order"
          cols="3"
          class="pb-0 mb-2"
        >
          <v-select
            dense
            hide-details
            outlined
            color="indigo"
            background-color="white"
            :items="invoiceTypes"
            :label="frappe._('Type')"
            v-model="invoiceType"
            :disabled="invoiceType == 'Return'"
          ></v-select>
        </v-col>
      </v-row>

      <div class="my-0 py-0 overflow-y-auto" style="max-height: 60vh">
        <template @mouseover="style = 'cursor: pointer'">
          <v-data-table
            :headers="items_headers"
            :items="items"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            show-expand
            item-key="posa_row_id"
            class="elevation-1"
            :items-per-page="itemsPerPage"
            hide-default-footer
          >
            <template v-slot:item.qty="{ item }">{{
              formtCurrency(item.qty)
            }}</template>
            <template v-slot:item.rate="{ item }">{{
              formtCurrency(item.rate)
            }}</template>
            <template v-slot:item.amount="{ item }">{{
              formtCurrency(item.qty * item.rate)
            }}</template>
            <template v-slot:item.posa_is_offer="{ item }">
              <v-simple-checkbox
                :value="!!item.posa_is_offer || !!item.posa_is_replace"
                disabled
              ></v-simple-checkbox>
            </template>

            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length" class="ma-0 pa-0">
                <v-row class="ma-0 pa-0">
                  <v-col cols="1">
                    <v-btn
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                      icon
                      color="red"
                      @click.stop="remove_item(item)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                  <v-spacer></v-spacer>
                  <v-col cols="1">
                    <v-btn
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                      icon
                      color="indigo lighten-1"
                      @click.stop="subtract_one(item)"
                    >
                      <v-icon>mdi-minus-circle-outline</v-icon>
                    </v-btn>
                  </v-col>
                  <v-col cols="1">
                    <v-btn
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                      icon
                      color="indigo lighten-1"
                      @click.stop="add_one(item)"
                    >
                      <v-icon>mdi-plus-circle-outline</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row class="ma-0 pa-0">
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Item Code')"
                      background-color="white"
                      hide-details
                      v-model="item.item_code"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('QTY')"
                      background-color="white"
                      hide-details
                      v-model.number="item.qty"
                      type="number"
                      @change="calc_sotck_gty(item, $event)"
                      :disabled="!!item.posa_is_offer || !!item.posa_is_replace"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-select
                      dense
                      background-color="white"
                      :label="frappe._('UOM')"
                      v-model="item.uom"
                      :items="item.item_uoms"
                      outlined
                      item-text="uom"
                      item-value="uom"
                      hide-details
                      @change="calc_uom(item, $event)"
                      :disabled="
                        !!invoice_doc.is_return ||
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace
                      "
                    >
                    </v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Rate')"
                      background-color="white"
                      hide-details
                      v-model.number="item.rate"
                      type="number"
                      :prefix="invoice_doc.currency"
                      @change="calc_prices(item, $event)"
                      id="rate"
                      :disabled="
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        !!item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_rate ||
                        !!invoice_doc.is_return
                          ? true
                          : false
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Discount Percentage')"
                      background-color="white"
                      hide-details
                      v-model.number="item.discount_percentage"
                      type="number"
                      @change="calc_prices(item, $event)"
                      id="discount_percentage"
                      :disabled="
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_item_discount ||
                        !!invoice_doc.is_return
                          ? true
                          : false
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Discount Amount')"
                      background-color="white"
                      hide-details
                      v-model.number="item.discount_amount"
                      type="number"
                      :prefix="invoice_doc.currency"
                      @change="calc_prices(item, $event)"
                      id="discount_amount"
                      :disabled="
                        !!item.posa_is_offer ||
                        !!item.posa_is_replace ||
                        !!item.posa_offer_applied ||
                        !pos_profile.posa_allow_user_to_edit_item_discount ||
                        !!invoice_doc.is_return
                          ? true
                          : false
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Price list Rate')"
                      background-color="white"
                      hide-details
                      v-model="item.price_list_rate"
                      type="number"
                      disabled
                      :prefix="invoice_doc.currency"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Available QTY')"
                      background-color="white"
                      hide-details
                      v-model="item.actual_qty"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Group')"
                      background-color="white"
                      hide-details
                      v-model="item.item_group"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Stock QTY')"
                      background-color="white"
                      hide-details
                      v-model="item.stock_qty"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Stock UOM')"
                      background-color="white"
                      hide-details
                      v-model="item.stock_uom"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col align="center" cols="4" v-if="item.posa_offer_applied">
                    <v-checkbox
                      dense
                      :label="frappe._('Offer Applied')"
                      v-model="item.posa_offer_applied"
                      readonly
                      hide-details
                      class="shrink mr-2 mt-0"
                    ></v-checkbox>
                  </v-col>
                  <v-col
                    cols="4"
                    v-if="item.has_serial_no == 1 || item.serial_no"
                  >
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Serial No QTY')"
                      background-color="white"
                      hide-details
                      v-model="item.serial_no_selected_count"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    v-if="item.has_serial_no == 1 || item.serial_no"
                  >
                    <v-autocomplete
                      v-model="item.serial_no_selected"
                      :items="item.serial_no_data"
                      item-text="serial_no"
                      outlined
                      dense
                      chips
                      color="indigo"
                      small-chips
                      :label="frappe._('Serial No')"
                      multiple
                      @change="set_serial_no(item)"
                    ></v-autocomplete>
                  </v-col>
                  <v-col
                    cols="4"
                    v-if="item.has_batch_no == 1 || item.batch_no"
                  >
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Batch No Available QTY')"
                      background-color="white"
                      hide-details
                      v-model="item.actual_batch_qty"
                      type="number"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="4"
                    v-if="item.has_batch_no == 1 || item.batch_no"
                  >
                    <v-text-field
                      dense
                      outlined
                      color="indigo"
                      :label="frappe._('Batch No Expiry Date')"
                      background-color="white"
                      hide-details
                      v-model="item.batch_no_expiry_date"
                      disabled
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="8"
                    v-if="item.has_batch_no == 1 || item.batch_no"
                  >
                    <v-autocomplete
                      v-model="item.batch_no"
                      :items="item.batch_no_data"
                      item-text="batch_no"
                      outlined
                      dense
                      color="indigo"
                      :label="frappe._('Batch No')"
                      @change="set_batch_qty(item, $event)"
                    >
                      <template v-slot:item="data">
                        <template>
                          <v-list-item-content>
                            <v-list-item-title
                              v-html="data.item.batch_no"
                            ></v-list-item-title>
                            <v-list-item-subtitle
                              v-html="
                                `Available QTY  '${data.item.batch_qty}' - Expiry Date ${data.item.expiry_date}`
                              "
                            ></v-list-item-subtitle>
                          </v-list-item-content>
                        </template>
                      </template>
                    </v-autocomplete>
                  </v-col>
                  <!-- Customized By Thirvusoft
                  Start -->
                  <!-- <v-col
                    cols="4"
                    v-if="
                      pos_profile.posa_allow_sales_order &&
                      invoiceType == 'Order'
                    "
                  >
                    <v-menu
                      ref="item_delivery_date"
                      v-model="item.item_delivery_date"
                      :close-on-content-click="false"
                      :return-value.sync="item.posa_delivery_date"
                      transition="scale-transition"
                      dense
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="item.posa_delivery_date"
                          :label="frappe._('Delivery Date')"
                          readonly
                          outlined
                          dense
                          clearable
                          color="indigo"
                          hide-details
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-date-picker
                        v-model="item.posa_delivery_date"
                        no-title
                        scrollable
                        color="indigo"
                        :min="frappe.datetime.now_date()"
                      >
                        <v-spacer></v-spacer>
                        <v-btn
                          text
                          color="primary"
                          @click="item.item_delivery_date = false"
                        >
                          Cancel
                        </v-btn>
                        <v-btn
                          text
                          color="primary"
                          @click="
                            [
                              $refs.item_delivery_date.save(
                                item.posa_delivery_date
                              ),
                              validate_due_date(item),
                            ]
                          "
                        >
                          OK
                        </v-btn>
                      </v-date-picker>
                    </v-menu>
                  </v-col> -->
                  <!-- End -->
                  <v-col
                    cols="8"
                    v-if="pos_profile.posa_display_additional_notes"
                  >
                    <v-textarea
                      class="pa-0"
                      outlined
                      dense
                      clearable
                      color="indigo"
                      auto-grow
                      rows="1"
                      :label="frappe._('Additional Notes')"
                      v-model="item.posa_notes"
                      :value="item.posa_notes"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </td>
            </template>
          </v-data-table>
        </template>
      </div>
    </v-card>
    <v-card class="cards mb-0 mt-3 py-0 grey lighten-5">
      <v-row no-gutters>
        <v-col cols="7">
          <v-row no-gutters class="pa-1 pt-2 pl-0">
            <v-col cols="6" class="pa-1">
              <v-text-field
                :value="formtCurrency(total_qty)"
                :label="frappe._('Total Qty')"
                outlined
                dense
                readonly
                hide-details
              ></v-text-field>
            </v-col>
            <!-- <v-col
              v-if="!pos_profile.posa_use_percentage_discount"
              cols="6"
              class="pa-1"
            >
              <v-text-field
                v-model="discount_amount"
                :label="frappe._('Additional Discount')"
                ref="discount"
                outlined
                dense
                hide-details
                type="number"
                :prefix="pos_profile.currency"
                :disabled="
                  !pos_profile.posa_allow_user_to_edit_additional_discount ||
                  discount_percentage_offer_name
                    ? true
                    : false
                "
              ></v-text-field>
            </v-col> -->
            <v-col
              v-if="pos_profile.posa_use_percentage_discount"
              cols="6"
              class="pa-1"
            >
              <v-text-field
                v-model="additional_discount_percentage"
                :label="frappe._('Additional Discount %')"
                ref="percentage_discount"
                outlined
                dense
                hide-details
                type="number"
                :disabled="
                  !pos_profile.posa_allow_user_to_edit_additional_discount ||
                  discount_percentage_offer_name
                    ? true
                    : false
                "
                @change="update_discount_umount"
              ></v-text-field>
<!--code start -->        
            </v-col>
            <!-- <v-col cols="6" class="pa-1">
              <v-text-field
                :value="formtCurrency(total_items_discount_amount)"
                :label="frappe._('Item Wise Discount Amount')"
                outlined
                dense
                readonly
                hide-details
                :prefix="pos_profile.currency"
              ></v-text-field>
            </v-col> -->
             <!-- <v-col
             cols="6"
              class="pa-1">
               <v-text-field
                v-model="add_disc_amt"
                :value="formtCurrency(add_disc_amt)"
                :label="frappe._('Overall Additional Discount ₹')"
                ref="add_disc_amt"
                outlined
                dense
                hide-details
                type="number"
                @change="change_dic_amount"
              ></v-text-field>
            </v-col> -->

            <v-col cols="6" class="pa-1">
              <v-text-field
                :value="formtCurrency(subtotal)"
                :label="frappe._('Total Amount')"
                outlined
                dense
                readonly
                hide-details
                class="text--red"
                :prefix="pos_profile.currency"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="5">
          <v-row no-gutters class="pa-1 pt-2 pl-0">
            <!-- <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="warning"
                dark
                @click="get_draft_invoices"
                >{{ __('Held') }}</v-btn
              >
            </v-col> -->
            <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                :class="{ 'disable-events': !pos_profile.posa_allow_return }"
                color="primary"
                dark
                @click="open_returns"
                >{{ __('Return') }}</v-btn
              >
            </v-col>
            <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="error"
                dark
                @click="cancel_dialog = true"
                >{{ __('Cancel') }}</v-btn
              >
            </v-col>
            <!-- <v-col cols="6" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="success"
                dark
                @click="new_invoice"
                >{{ __('Save/New') }}</v-btn
              >
            </v-col> -->
            <v-col cols="12" class="pa-1">
              <v-btn
                block
                class="pa-0"
                color="success"
                @click="show_payment"
                dark
                >{{ __('PAY') }}</v-btn
              >
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
import Customer from './Customer.vue';

export default {
  data() {
    return {
      pos_profile: '',
      pos_opening_shift: '',
      stock_settings: '',
      thirvu_settings: '',
      feedback_required: 0,
      invoice_doc: '',
      return_doc: '',
      customer: '',
      customer_info: '',
      discount_amount: 0,
      additional_discount_percentage: 0,
      add_disc_amt:0,
      total_tax: 0,
      items: [],
      posOffers: [],
      posa_offers: [],
      posa_coupons: [],
      allItems: [],
      discount_percentage_offer_name: null,
      invoiceTypes: ['Invoice', 'Order'],
      invoiceType: 'Invoice',
      itemsPerPage: 1000,
      expanded: [],
      singleExpand: true,
      cancel_dialog: false,
      items_headers: [
        {
          text: __('Name'),
          align: 'start',
          sortable: true,
          value: 'item_name',
        },
        { text: __('QTY'), value: 'qty', align: 'center' },
        { text: __('UOM'), value: 'uom', align: 'center' },
        { text: __('Rate'), value: 'rate', align: 'center' },
        { text: __('Amount'), value: 'amount', align: 'center' },
        // Customized By Thirvusoft
        // Start
        // { text: __('is Offer'), value: 'posa_is_offer', align: 'center' },
        // End
      ],
    };
  },

  components: {
    Customer,
  },

  computed: {
    total_qty() {
      this.close_payments();
      let qty = 0;
      this.items.forEach((item) => {
        qty += item.qty;
      });
      return flt(qty).toFixed(2);
    },
    Total() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.rate;
      });
      return flt(sum).toFixed(2);
    },
    subtotal() {
      this.close_payments();
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.rate;
      });
      sum -= flt(this.discount_amount);
      return flt(sum).toFixed(2);
    },
    total_items_discount_amount() {
      let sum = 0;
      this.items.forEach((item) => {
        sum += item.qty * item.discount_amount;
      });
      return flt(sum).toFixed(2);
    },
  },

  methods: {
    remove_item(item) {
      const index = this.items.findIndex(
        (el) => el.posa_row_id == item.posa_row_id
      );
      if (index >= 0) {
        this.items.splice(index, 1);
      }
      const idx = this.expanded.findIndex(
        (el) => el.posa_row_id == item.posa_row_id
      );
      if (idx >= 0) {
        this.expanded.splice(idx, 1);
      }
    },

    add_one(item) {
      item.qty++;
      if (item.qty == 0) {
        this.remove_item(item);
      }
      this.calc_sotck_gty(item, item.qty);
      this.$forceUpdate();
    },
    subtract_one(item) {
      item.qty--;
      if (item.qty == 0) {
        this.remove_item(item);
      }
      this.calc_sotck_gty(item, item.qty);
      this.$forceUpdate();
    },

     add_item: function add_item(item) {
        if (!item.uom) {
          item.uom = item.stock_uom;
        }
              const index = this.items.findIndex(
        (el) =>
          el.item_code === item.item_code &&
          el.batch_no === item.ts_current_batch &&
          el.uom === item.uom &&
          !el.posa_is_offer &&
          !el.posa_is_replace
      );
      if (index === -1) {

          var new_item = this.get_new_item(item);
          if (item.has_serial_no && item.to_set_serial_no) {
            new_item.serial_no_selected = [];
            new_item.serial_no_selected.push(item.to_set_serial_no);
            item.to_set_serial_no = null;
          }
          this.items.unshift(new_item);
          this.update_item_detail(new_item);
        } else {
          var cur_item = this.items[index];
          this.update_items_details([cur_item]);
          if (item.has_serial_no && item.to_set_serial_no) {
            if (cur_item.serial_no_selected.includes(item.to_set_serial_no)) {
              evntBus.$emit('show_mesage', {
                text: __("This Serial Number {0} has already been added!", [
                  item.to_set_serial_no ]),
                color: 'warning',
              });
              item.to_set_serial_no = null;
              return;
            }
            cur_item.serial_no_selected.push(item.to_set_serial_no);
            item.to_set_serial_no = null;
          }
          if (!cur_item.has_batch_no) {
            cur_item.qty += item.qty || 1;
            this.calc_sotck_gty(cur_item, cur_item.qty);
          } else {
            if (
              cur_item.stock_qty < cur_item.actual_batch_qty ||
              !cur_item.batch_no
            ) {
              cur_item.qty += item.qty || 1;
              this.calc_sotck_gty(cur_item, cur_item.qty);
            } else {
              var new_item$1 = this.get_new_item(cur_item);
              new_item$1.batch_no = '';
              new_item$1.batch_no_expiry_date = '';
              new_item$1.actual_batch_qty = '';
              new_item$1.qty = item.qty || 1;
              this.items.unshift(new_item$1);
            }
          }
          this.set_serial_no(cur_item);
        }
        this.$forceUpdate();
      },

   get_new_item: function get_new_item(item) {
        var new_item = Object.assign({}, item);
        if (!item.qty) {
          item.qty = 1;
        }
        if (!item.posa_is_offer) {
          item.posa_is_offer = 0;
        }
        if (!item.posa_is_replace) {
          item.posa_is_replace = '';
        }
        new_item.stock_qty = item.qty;
        new_item.discount_amount = 0;
        new_item.discount_percentage = 0;
        new_item.discount_amount_per_item = 0;
        new_item.price_list_rate = item.rate;
        new_item.qty = item.qty;
        new_item.uom = item.uom ? item.uom : item.stock_uom;
        new_item.actual_batch_qty = '';
        new_item.conversion_factor = 1;
        new_item.posa_offers = JSON.stringify([]);
        new_item.posa_offer_applied = 0;
        new_item.posa_is_offer = item.posa_is_offer;
        new_item.posa_is_replace = item.posa_is_replace || null;
        new_item.is_free_item = 0;
        new_item.posa_notes = '';
        new_item.posa_delivery_date = '';
        new_item.posa_row_id = this.makeid(20);
        if (
          (!this.pos_profile.posa_auto_set_batch && new_item.has_batch_no) ||
          new_item.has_serial_no
        ) {
          this.expanded.push(new_item);
        }
        return new_item;
      },


    cancel_invoice: function cancel_invoice() {
        var doc = this.get_invoice_doc();
        this.invoiceType = 'Invoice';
        this.invoiceTypes = ['Invoice', 'Order'];
        if (doc.name && this.pos_profile.posa_allow_delete) {
          frappe.call({
            method: 'posawesome.posawesome.api.posapp.delete_invoice',
            args: { invoice: doc.name },
            async: true,
            callback: function (r) {
              if (r.message) {
                evntBus.$emit('show_mesage', {
                  text: r.message,
                  color: 'warning',
                });
              }
            },
          });
        }
        this.items = [];
        this.posa_offers = [];
        evntBus.$emit('set_pos_coupons', []);
        this.posa_coupons = [];
        this.customer = this.pos_profile.customer;
        this.invoice_doc = '';
        this.return_doc = '';
        this.discount_amount = 0;
        this.additional_discount_percentage = 0;
        evntBus.$emit('set_customer_readonly', false);
        this.cancel_dialog = false;
      },

       new_invoice: function new_invoice(data) {
        var this$1 = this;
        if ( data === void 0 ) data = {};

        evntBus.$emit('set_customer_readonly', false);
        this.expanded = [];
        this.posa_offers = [];
        evntBus.$emit('set_pos_coupons', []);
        this.posa_coupons = [];
        this.return_doc = '';
        var doc = this.get_invoice_doc();
        if (doc.name) {
          this.update_invoice(doc);
        } else {
          if (doc.items.length) {
            this.update_invoice(doc);
          }
        }
        if (!data.name && !data.is_return) {
          this.items = [];
          this.customer = this.pos_profile.customer;
          this.invoice_doc = '';
          this.discount_amount = 0;
          this.additional_discount_percentage = 0;
          this.invoiceType = 'Invoice';
          this.invoiceTypes = ['Invoice', 'Order'];
        } else {
          if (data.is_return) {
            evntBus.$emit('set_customer_readonly', true);
            this.invoiceType = 'Return';
            this.invoiceTypes = ['Return'];
          }
          this.invoice_doc = data;
          this.items = data.items;
          this.update_items_details(this.items);
          this.posa_offers = data.posa_offers || [];
          this.items.forEach(function (item) {
            if (!item.posa_row_id) {
              item.posa_row_id = this$1.makeid(20);
            }
            if (item.batch_no) {
              this$1.set_batch_qty(item, item.batch_no);
            }
          });
          this.customer = data.customer;
          this.add_disc_amt = data.discount_amount;
          this.discount_amount = data.discount_amount;
          this.additional_discount_percentage =
            data.additional_discount_percentage;
          this.items.forEach(function (item) {
            if (item.serial_no) {
              item.serial_no_selected = [];
              var serial_list = item.serial_no.split('\n');
              serial_list.forEach(function (element) {
                if (element.length) {
                  item.serial_no_selected.push(element);
                }
              });
              item.serial_no_selected_count = item.serial_no_selected.length;
            }
          });
        }
      },

   get_invoice_doc: function get_invoice_doc() {
        var doc = {};
        if (this.invoice_doc.name) {
          doc = Object.assign({}, this.invoice_doc);
        }
        //creating sales invoice
        doc.doctype = 'Sales Invoice';
        doc.is_pos = 1;
        doc.ignore_pricing_rule = 1;
        doc.company = doc.company || this.pos_profile.company;
        doc.pos_profile = doc.pos_profile || this.pos_profile.name;
        doc.campaign = doc.campaign || this.pos_profile.campaign;
        doc.currency = doc.currency || this.pos_profile.currency;
        doc.naming_series = doc.naming_series || this.pos_profile.naming_series;
        doc.customer = this.customer;
        doc.items = this.get_invoice_items();
        doc.total = this.subtotal;
        doc.discount_amount = flt(this.discount_amount);
        doc.additional_discount_percentage = flt(
          this.additional_discount_percentage
        );
        doc.posa_pos_opening_shift = this.pos_opening_shift.name;
        doc.payments = this.get_payments();
        doc.taxes = [];
        doc.is_return = this.invoice_doc.is_return;
        doc.return_against = this.invoice_doc.return_against;
        doc.posa_offers = this.posa_offers;
        doc.posa_coupons = this.posa_coupons;
        return doc;
      },

       get_invoice_items: function get_invoice_items() {
        var items_list = [];
        this.items.forEach(function (item) {
          var new_item = {
            item_code: item.item_code,
            posa_row_id: item.posa_row_id,
            posa_offers: item.posa_offers,
            posa_offer_applied: item.posa_offer_applied,
            posa_is_offer: item.posa_is_offer,
            posa_is_replace: item.posa_is_replace,
            is_free_item: item.is_free_item,
            qty: item.qty,
            rate: item.rate,
            uom: item.uom,
            amount: item.qty * item.rate,
            conversion_factor: item.conversion_factor,
            serial_no: item.serial_no,
            discount_percentage: item.discount_percentage,
            discount_amount: item.discount_amount,
            batch_no: item.batch_no,
            posa_notes: item.posa_notes,
            posa_delivery_date: item.posa_delivery_date,
            price_list_rate: item.price_list_rate,
            warehouse: item.warehouse
          };
          items_list.push(new_item);
        });
        return items_list;
      },

     get_payments: function get_payments() {
        var payments = [];
        this.pos_profile.payments.forEach(function (payment) {
          payments.push({
            amount: 0,
            mode_of_payment: payment.mode_of_payment,
            default: payment.default,
            account: '',
          });
        });
        return payments;
      },

    update_invoice: function update_invoice(doc) {
        var vm = this;
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.update_invoice',
          args: {
            data: doc,
          },
          async: false,
          callback: function (r) {
            if (r.message) {
              vm.invoice_doc = r.message[0];
              vm.thirvu_settings = r.message[1]
              vm.feedback_required = r.message[2]
            }
          },
        });
        return this.invoice_doc;
      },


     proces_invoice: function proces_invoice() {
        var doc = this.get_invoice_doc();
        if (doc.name) {
          return this.update_invoice(doc);
        } else {
          return this.update_invoice(doc);
        }
      },

    show_payment: function show_payment() {

        if (!this.customer) {
          evntBus.$emit('show_mesage', {
            text: __("There is no Customer !"),
            color: 'error',
          });
          return;
        }

        if (!this.items.length) {
          evntBus.$emit('show_mesage', {
            text: __("There is no Items !"),
            color: 'error',
          });
          return;
        }
         // Customized By Thirvusoft
         // Start
         frappe.db.get_single_value("Thirvu Retail Settings","allow_display_customer_transaction_history").then(value =>{
          if(value==1){
             frappe.call({
                 method:"posawesome.posawesome.api.posapp.customer_transaction_history",
                 args:{
                     customer:this.customer
                     },
                 callback: function(r){
                       var dialog_trans = new frappe.ui.Dialog({
                       title: "Customer transaction history",
                       fields:[
                       {
                       fieldname:'table',
                       fieldtype:'HTML',
                       label:'Table'
                      },
                       ],
                       primary_action : function(data){
                       dialog_trans.hide()
                       }
                   });
              if(r.message[1]){
                var template = r.message[3]
                dialog_trans.set_df_property('table', 'options', frappe.render(template,{}))
                dialog_trans.show();
              }
                   }
           });
          }
         })
         //End
        
        if (!this.validate()) {
          return;
        }
        evntBus.$emit('show_payment', 'true');
        var invoice_doc = this.proces_invoice();
        var thirvu_settings = this.thirvu_settings
        var feedback_required = this.feedback_required
        
        evntBus.$emit('send_invoice_doc_payment', invoice_doc,thirvu_settings, feedback_required);
      },

     validate: function validate() {
        var this$1 = this;

        var value = true;
        this.items.forEach(function (item) {
          if (this$1.stock_settings.allow_negative_stock != 1) {
            if (
              this$1.invoiceType == 'Invoice' &&
              ((item.is_stock_item && item.stock_qty && !item.actual_qty) ||
                (item.is_stock_item && item.stock_qty > item.actual_qty))
            ) {
              evntBus.$emit('show_mesage', {
                text: __(
                  "The existing quantity '{0}' for item '{1}' is not enough",
                  [item.actual_qty, item.item_name]
                ),
                color: 'error',
              });
              value = false;
            }
          }
          if (
            item.max_discount > 0 &&
            item.discount_percentage > item.max_discount
          ) {
            evntBus.$emit('show_mesage', {
              text: __("Maximum discount for Item {0} is {1}%", [
                item.item_name,
                item.max_discount ]),
              color: 'error',
            });
            value = false;
          }
          if (item.has_serial_no) {
            if (
              !this$1.invoice_doc.is_return &&
              (!item.serial_no_selected ||
                item.stock_qty != item.serial_no_selected.length)
            ) {
              evntBus.$emit('show_mesage', {
                text: __("Selected serial numbers of item {0} is incorrect", [
                  item.item_name ]),
                color: 'error',
              });
              value = false;
            }
          }
          if (item.has_batch_no) {
            if (item.stock_qty > item.actual_batch_qty) {
              evntBus.$emit('show_mesage', {
                text: __(
                  "The existing batch quantity of item {0} is not enough",
                  [item.item_name]
                ),
                color: 'error',
              });
              value = false;
            }
          }
          if (this$1.pos_profile.posa_allow_user_to_edit_additional_discount) {
            var clac_percentage = (this$1.discount_amount / this$1.Total) * 100;
            if (clac_percentage > this$1.pos_profile.posa_max_discount_allowed) {
              evntBus.$emit('show_mesage', {
                text: __("The discount should not be higher than {0}%", [
                  this$1.pos_profile.posa_max_discount_allowed ]),
                color: 'error',
              });
              value = false;
            }
          }
          if (this$1.invoice_doc.is_return) {
            if (this$1.subtotal >= 0) {
              evntBus.$emit('show_mesage', {
                text: __("Return Invoice Total Not Correct"),
                color: 'error',
              });
              value = false;
              return value;
            }
            if (this$1.subtotal * -1 > this$1.return_doc.total) {
              evntBus.$emit('show_mesage', {
                text: __("Return Invoice Total should not be higher than {0}", [
                  this$1.return_doc.total ]),
                color: 'error',
              });
              value = false;
              return value;
            }
            this$1.items.forEach(function (item) {
              var return_item = this$1.return_doc.items.find(
                function (element) { return element.item_code == item.item_code; }
              );

              if (!return_item) {
                evntBus.$emit('show_mesage', {
                  text: __(
                    "The item {0} cannot be returned because it is not in the invoice {1}",
                    [item.item_name, this$1.return_doc.name]
                  ),
                  color: 'error',
                });
                value = false;
                return value;
              } else if (item.qty * -1 > return_item.qty || item.qty >= 0) {
                evntBus.$emit('show_mesage', {
                  text: __("The QTY of the item {0} cannot be greater than {1}", [
                    item.item_name,
                    return_item.qty ]),
                  color: 'error',
                });
                value = false;
                return value;
              }
            });
          }
        });
        return value;
      },

    get_draft_invoices: function get_draft_invoices() {
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_draft_invoices',
          args: {
            pos_opening_shift: this.pos_opening_shift.name,
          },
          async: false,
          callback: function (r) {
            if (r.message) {
              evntBus.$emit('open_drafts', r.message);
            }
          },
        });
      },

    open_returns: function open_returns() {
        evntBus.$emit('open_returns', this.pos_profile.company);
      },

    close_payments: function close_payments() {
        evntBus.$emit('show_payment', 'false');
      },

    update_items_details: function update_items_details(items) {
        if (!items.length > 0) {
          return;
        }
        var vm = this;
        if (!vm.pos_profile) { return; }
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_items_details',
          async: false,
          args: {
            pos_profile: vm.pos_profile,
            items_data: items,
          },
          callback: function (r) {
            if (r.message) {
              items.forEach(function (item) {
                var updated_item = r.message.find(
                  function (element) { return element.posa_row_id == item.posa_row_id; }
                );
                item.actual_qty = updated_item.actual_qty;
                item.serial_no_data = updated_item.serial_no_data;
                item.batch_no_data = updated_item.batch_no_data;
                item.item_uoms = updated_item.item_uoms;
                item.has_batch_no = updated_item.has_batch_no;
                item.has_serial_no = updated_item.has_serial_no;
              });
            }
          },
        });
      },

      update_item_detail: function update_item_detail(item) {
        var vm = this;
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_item_detail',
          args: {
            warehouse: item.warehouse,
            doc: this.get_invoice_doc(),
            price_list: this.pos_profile.price_list,
            item: {
              item_code: item.item_code,
              customer: this.customer,
              doctype: 'Sales Invoice',
              name: 'New Sales Invoice 1',
              company: this.pos_profile.company,
              conversion_rate: 1,
              qty: item.qty,
              price_list_rate: item.price_list_rate,
              child_docname: 'New Sales Invoice Item 1',
              cost_center: this.pos_profile.cost_center,
              currency: this.pos_profile.currency,
              // plc_conversion_rate: 1,
              pos_profile: this.pos_profile.name,
              price_list: this.pos_profile.selling_price_list,
              uom: item.uom,
              tax_category: '',
              transaction_type: 'selling',
              update_stock: this.pos_profile.update_stock,
              price_list: this.get_price_list(),
              has_batch_no: item.has_batch_no,
              serial_no: item.serial_no,
              batch_no: item.ts_current_batch,
              is_stock_item: item.is_stock_item,
            },
          },
          callback: function (r) {
            if (r.message) {
              var data = r.message;
              if (
                item.has_batch_no &&
                vm.pos_profile.posa_auto_set_batch &&
                !item.batch_no &&
                data.batch_no
              ) {
                item.batch_no = data.batch_no;
                vm.set_batch_qty(item, item.batch_no, false);
              }
              if (data.has_pricing_rule) ; else if (
                vm.pos_profile.posa_apply_customer_discount &&
                vm.customer_info.posa_discount > 0 &&
                vm.customer_info.posa_discount <= 100
              ) {
                if (
                  item.posa_is_offer == 0 &&
                  !item.posa_is_replace &&
                  item.posa_offer_applied == 0
                ) {
                  if (item.max_discount > 0) {
                    item.discount_percentage =
                      item.max_discount < vm.customer_info.posa_discount
                        ? item.max_discount
                        : vm.customer_info.posa_discount;
                  } else {
                    item.discount_percentage = vm.customer_info.posa_discount;
                  }
                }
              }
              if (!item.btach_price) {
                if (
                  !item.is_free_item &&
                  !item.posa_is_offer &&
                  !item.posa_is_replace
                ) {
                  item.price_list_rate = data.price_list_rate;
                }
              }
              item.last_purchase_rate = data.last_purchase_rate;
              item.projected_qty = data.projected_qty;
              item.reserved_qty = data.reserved_qty;
              item.conversion_factor = data.conversion_factor;
              item.stock_qty = data.stock_qty;
              item.actual_qty = data.actual_qty;
              item.stock_uom = data.stock_uom;
              (item.has_serial_no = data.has_serial_no),
                (item.has_batch_no = data.has_batch_no),
                vm.calc_item_price(item);
            }
          },
        });
      },

     fetch_customer_details: function fetch_customer_details() {
        var vm = this;
        if (this.customer) {
          frappe.call({
            method: 'posawesome.posawesome.api.posapp.get_customer_info',
            args: {
              customer: vm.customer,
            },
            async: false,
            callback: function (r) {
              var message = r.message;
              if (!r.exc) {
                vm.customer_info = Object.assign({}, message);
             }
              vm.update_price_list();
            },
          });
        }
      },
    get_price_list: function get_price_list() {
        var price_list = this.pos_profile.selling_price_list;
        if (this.customer_info && this.pos_profile) {
          var ref =
            this.customer_info;
          var customer_price_list = ref.customer_price_list;
          var customer_group_price_list = ref.customer_group_price_list;
          var pos_price_list = this.pos_profile.selling_price_list;
          if (customer_price_list && customer_price_list != pos_price_list) {
            price_list = customer_price_list;
          } else if (
            customer_group_price_list &&
            customer_group_price_list != pos_price_list
          ) {
            price_list = customer_group_price_list;
          }
        }
        return price_list;
      },

    update_price_list: function update_price_list() {
        var price_list = this.get_price_list();
        if (price_list == this.pos_profile.selling_price_list) {
          price_list = null;
        }
        evntBus.$emit('update_customer_price_list', price_list);
      },
    update_discount_umount: function update_discount_umount() {
          var value = flt(this.additional_discount_percentage);
        if (value >= -100 && value <= 100) {
          this.discount_amount = (this.Total * value) / 100;
        } else {
          this.additional_discount_percentage = 0;
          this.discount_amount = 0;
        }
      },
  // code start

      change_dic_amount(){
        
          var value = flt(this.additional_discount_percentage);
         
         this.additional_discount_percentage =(this.add_disc_amt * 100)/ this.Total;
                                 
      },
  //code End
    calc_prices: function calc_prices(item, value, $event) {
        if (event.target.id === 'rate') {
          item.discount_percentage = 0;
          if (value < item.price_list_rate) {
            item.discount_amount = (
              flt(item.price_list_rate) - flt(value)
            ).toFixed(2);
          } else if (value < 0) {
            item.rate = item.price_list_rate;
            item.discount_amount = 0;
          } else if (value > item.price_list_rate) {
            item.discount_amount = 0;
          }
        } else if (event.target.id === 'discount_amount') {
          if (value < 0) {
            item.discount_amount = 0;
            item.discount_percentage = 0;
          } else {
            item.rate = flt(item.price_list_rate) - flt(value);
            item.discount_percentage = 0;
          }
        } else if (event.target.id === 'discount_percentage') {
          if (value < 0) {
            item.discount_amount = 0;
            item.discount_percentage = 0;
          } else {
            item.rate = (
              flt(item.price_list_rate) -
              (flt(item.price_list_rate) * flt(value)) / 100
            ).toFixed(2);
            item.discount_amount = (
              flt(item.price_list_rate) - flt(item.rate)
            ).toFixed(2);
          }
        }
      },

     calc_item_price: function calc_item_price(item) {
        if (!item.posa_offer_applied) {
          if (item.price_list_rate) {
            item.rate = item.price_list_rate;
          }
        }
        if (item.discount_percentage) {
          item.rate =
            flt(item.price_list_rate) -
            (flt(item.price_list_rate) * flt(item.discount_percentage)) / 100;
          item.discount_amount = (
            flt(item.price_list_rate) - flt(item.rate)
          ).toFixed(2);
        } else if (item.discount_amount) {
          item.rate = (
            flt(item.price_list_rate) - flt(item.discount_amount)
          ).toFixed(2);
        }
      },

     calc_uom: function calc_uom(item, value) {
        var new_uom = item.item_uoms.find(function (element) { return element.uom == value; });
        item.conversion_factor = new_uom.conversion_factor;
        if (!item.posa_offer_applied) {
          item.discount_amount = 0;
          item.discount_percentage = 0;
        }
        if (item.btach_price) {
          item.price_list_rate = item.btach_price * new_uom.conversion_factor;
        }
        this.update_item_detail(item);
      },

      calc_sotck_gty: function calc_sotck_gty(item, value) {
        item.stock_qty = item.conversion_factor * value;
      },

      set_serial_no: function set_serial_no(item) {
        if (!item.has_serial_no) { return; }
        item.serial_no = '';
        item.serial_no_selected.forEach(function (element) {
          item.serial_no += element + '\n';
        });
        item.serial_no_selected_count = item.serial_no_selected.length;
        if (item.serial_no_selected_count != item.stock_qty) {
          evntBus.$emit('show_mesage', {
            text: __("Selected Serial No QTY is {0} it should be {1}", [
              item.serial_no_selected_count,
              item.stock_qty ]),
            color: 'warning',
          });
        }
      },

   set_batch_qty: function set_batch_qty(item, value, update) {
        if ( update === void 0 ) update = true;

        var batch_no = item.batch_no_data.find(
          function (element) { return element.batch_no == value; }
        );
        item.actual_batch_qty = batch_no.batch_qty;
        item.batch_no_expiry_date = batch_no.expiry_date;
      // Customized By Thirvusoft
      // Start
      if (batch_no.ts_selling_price) {
        item.btach_price = batch_no.ts_selling_price;
        item.price_list_rate = batch_no.ts_selling_price;
        item.rate = batch_no.ts_selling_price;
      // End
        }else if (update) {
          item.btach_price = null;
          this.update_item_detail(item);
        }
      },

    formtCurrency: function formtCurrency(value) {
        value = parseFloat(value);
        return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
      },
    // Customized By Thirvusoft
    // Start
    shortOpenPayment: function shortOpenPayment(e) {
        if (e.key === 'F7') {
          e.preventDefault();
          this.show_payment();
        }
      },
    // End

    shortDeleteFirstItem: function shortDeleteFirstItem(e) {
        if (e.key === 'd' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          this.remove_item(this.items[0]);
        }
      },
      // Customized By Thirvusoft
      // Start
      shortOpenReturn: function shortOpenReturn(e) {
        if (e.key === 'F9') {
          e.preventDefault();
          this.open_returns();
        }
      },
      shortCancelInvoice: function shortCancelInvoice(e) {
        if (e.key === 'c' && (e.altKey)) {
          e.preventDefault();
          this.cancel_invoice();
        }
      },
      //  End

    shortOpenFirstItem: function shortOpenFirstItem(e) {
        if (e.key === 'a' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          this.expanded = [];
          this.expanded.push(this.items[0]);
        }
      },

    shortSelectDiscount: function shortSelectDiscount(e) {
        if (e.key === 'z' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          this.$refs.discount.focus();
        }
      },

    makeid: function makeid(length) {
        var result = '';
        var characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
          result += characters.charAt(
            Math.floor(Math.random() * charactersLength)
          );
        }
        return result;
      },

    checkOfferIsAppley: function checkOfferIsAppley(item, offer) {
        var this$1 = this;

        var applied = false;
        var item_offers = JSON.parse(item.posa_offers);
        var loop = function () {
          var row_id = list[i];

          var exist_offer = this$1.posa_offers.find(function (el) { return row_id == el.row_id; });
          if (exist_offer && exist_offer.offer_name == offer.name) {
            applied = true;
            return 'break';
          }
        };

        for (var i = 0, list = item_offers; i < list.length; i += 1) {
          var returned = loop();

          if ( returned === 'break' ) break;
        }
        return applied;
      },

    handelOffers: function handelOffers() {
        var this$1 = this;

        var offers = [];
        this.posOffers.forEach(function (offer) {
          if (offer.apply_on === 'Item Code') {
            var itemOffer = this$1.getItemOffer(offer);
            if (itemOffer) {
              offers.push(itemOffer);
            }
          } else if (offer.apply_on === 'Item Group') {
            var groupOffer = this$1.getGroupOffer(offer);
            if (groupOffer) {
              offers.push(groupOffer);
            }
          } else if (offer.apply_on === 'Brand') {
            var brandOffer = this$1.getBrandOffer(offer);
            if (brandOffer) {
              offers.push(brandOffer);
            }
          } else if (offer.apply_on === 'Transaction') {
            var transactionOffer = this$1.getTransactionOffer(offer);
            if (transactionOffer) {
              offers.push(transactionOffer);
            }
          }
        });

        this.setItemGiveOffer(offers);
        this.updatePosOffers(offers);
      },

    setItemGiveOffer: function setItemGiveOffer(offers) {
        var this$1 = this;

        // Set item give offer for replace
        offers.forEach(function (offer) {
          if (
            offer.apply_on == 'Item Code' &&
            offer.apply_type == 'Item Code' &&
            offer.replace_item
          ) {
            offer.give_item = offer.item;
            offer.apply_item_code = offer.item;
          } else if (
            offer.apply_on == 'Item Group' &&
            offer.apply_type == 'Item Group' &&
            offer.replace_cheapest_item
          ) {
            var offerItemCode = this$1.getCheapestItem(offer).item_code;
            offer.give_item = offerItemCode;
            offer.apply_item_code = offerItemCode;
          }
        });
      },

     getCheapestItem: function getCheapestItem(offer) {
        var this$1 = this;

        var itemsRowID;
        if (typeof offer.items === 'string') {
          itemsRowID = JSON.parse(offer.items);
        } else {
          itemsRowID = offer.items;
        }
        var itemsList = [];
        itemsRowID.forEach(function (row_id) {
          itemsList.push(this$1.getItemFromRowID(row_id));
        });
        var result = itemsList.reduce(function (res, obj) {
          return !obj.posa_is_replace &&
            !obj.posa_is_offer &&
            obj.price_list_rate < res.price_list_rate
            ? obj
            : res;
        });
        return result;
      },

    getItemFromRowID: function getItemFromRowID(row_id) {
        var item = this.items.find(function (el) { return el.posa_row_id == row_id; });
        return item;
      },

    checkQtyAnountOffer: function checkQtyAnountOffer(offer, qty, amount) {
        var min_qty = false;
        var max_qty = false;
        var min_amt = false;
        var max_amt = false;
        var applys = [];

        if (offer.min_qty || offer.min_qty == 0) {
          if (qty >= offer.min_qty) {
            min_qty = true;
          }
          applys.push(min_qty);
        }

        if (offer.max_qty > 0) {
          if (qty <= offer.max_qty) {
            max_qty = true;
          }
          applys.push(max_qty);
        }

        if (offer.min_amt > 0) {
          if (amount >= offer.min_amt) {
            min_amt = true;
          }
          applys.push(min_amt);
        }

        if (offer.max_amt > 0) {
          if (amount <= offer.max_amt) {
            max_amt = true;
          }
          applys.push(max_amt);
        }
        var apply = false;
        if (!applys.includes(false)) {
          apply = true;
        }
        var res = {
          apply: apply,
          conditions: { min_qty: min_qty, max_qty: max_qty, min_amt: min_amt, max_amt: max_amt },
        };
        return res;
      },

    checkOfferCoupon: function checkOfferCoupon(offer) {
        if (offer.coupon_based) {
          var coupon = this.posa_coupons.find(
            function (el) { return offer.name == el.pos_offer; }
          );
          if (coupon) {
            offer.coupon = coupon.coupon;
            return true;
          } else {
            return false;
          }
        } else {
          offer.coupon = null;
          return true;
        }
      },

    
    getItemOffer: function getItemOffer(offer) {
        var this$1 = this;

        var apply_offer = null;
        if (offer.apply_on === 'Item Code') {
          if (this.checkOfferCoupon(offer)) {
            this.items.forEach(function (item) {
              if (!item.posa_is_offer && item.item_code === offer.item) {
                var items = [];
                if (
                  offer.offer === 'Item Price' &&
                  item.posa_offer_applied &&
                  !this$1.checkOfferIsAppley(item, offer)
                ) ; else {
                  var res = this$1.checkQtyAnountOffer(
                    offer,
                    item.stock_qty,
                    item.stock_qty * item.price_list_rate
                  );
                  if (res.apply) {
                    items.push(item.posa_row_id);
                    offer.items = items;
                    apply_offer = offer;
                  }
                }
              }
            });
          }
        }
        return apply_offer;
      },

    getGroupOffer: function getGroupOffer(offer) {
        var this$1 = this;

        var apply_offer = null;
        if (offer.apply_on === 'Item Group') {
          if (this.checkOfferCoupon(offer)) {
            var items = [];
            var total_count = 0;
            var total_amount = 0;
            this.items.forEach(function (item) {
              if (!item.posa_is_offer && item.item_group === offer.item_group) {
                if (
                  offer.offer === 'Item Price' &&
                  item.posa_offer_applied &&
                  !this$1.checkOfferIsAppley(item, offer)
                ) ; else {
                  total_count += item.stock_qty;
                  total_amount += item.stock_qty * item.price_list_rate;
                  items.push(item.posa_row_id);
                }
              }
            });
            if (total_count || total_amount) {
              var res = this.checkQtyAnountOffer(
                offer,
                total_count,
                total_amount
              );
              if (res.apply) {
                offer.items = items;
                apply_offer = offer;
              }
            }
          }
        }
        return apply_offer;
      },

    getBrandOffer: function getBrandOffer(offer) {
        var this$1 = this;

        var apply_offer = null;
        if (offer.apply_on === 'Brand') {
          if (this.checkOfferCoupon(offer)) {
            var items = [];
            var total_count = 0;
            var total_amount = 0;
            this.items.forEach(function (item) {
              if (!item.posa_is_offer && item.brand === offer.brand) {
                if (
                  offer.offer === 'Item Price' &&
                  item.posa_offer_applied &&
                  !this$1.checkOfferIsAppley(item, offer)
                ) ; else {
                  total_count += item.stock_qty;
                  total_amount += item.stock_qty * item.price_list_rate;
                  items.push(item.posa_row_id);
                }
              }
            });
            if (total_count || total_amount) {
              var res = this.checkQtyAnountOffer(
                offer,
                total_count,
                total_amount
              );
              if (res.apply) {
                offer.items = items;
                apply_offer = offer;
              }
            }
          }
        }
        return apply_offer;
      },
    getTransactionOffer: function getTransactionOffer(offer) {
        var apply_offer = null;
        if (offer.apply_on === 'Transaction') {
          if (this.checkOfferCoupon(offer)) {
            var total_qty = 0;
            this.items.forEach(function (item) {
              if (!item.posa_is_offer && !item.posa_is_replace) {
                total_qty += item.stock_qty;
              }
            });
            var items = [];
            var total_count = total_qty;
            var total_amount = this.Total;
            if (total_count || total_amount) {
              var res = this.checkQtyAnountOffer(
                offer,
                total_count,
                total_amount
              );
              if (res.apply) {
                this.items.forEach(function (item) {
                  items.push(item.posa_row_id);
                });
                offer.items = items;
                apply_offer = offer;
              }
            }
          }
        }
        return apply_offer;
      },

   updatePosOffers: function updatePosOffers(offers) {
        evntBus.$emit('update_pos_offers', offers);
      },

      updateInvoiceOffers: function updateInvoiceOffers(offers) {
        var this$1 = this;

        this.posa_offers.forEach(function (invoiceOffer) {
          var existOffer = offers.find(
            function (offer) { return invoiceOffer.row_id == offer.row_id; }
          );
          if (!existOffer) {
            this$1.removeApplyOffer(invoiceOffer);
          }
        });
        offers.forEach(function (offer) {
          var existOffer = this$1.posa_offers.find(
            function (invoiceOffer) { return invoiceOffer.row_id == offer.row_id; }
          );
          if (existOffer) {
            existOffer.items = JSON.stringify(offer.items);
            if (
              existOffer.offer === 'Give Product' &&
              existOffer.give_item &&
              existOffer.give_item != offer.give_item
            ) {
              var item_to_remove = this$1.items.find(
                function (item) { return item.posa_row_id == existOffer.give_item_row_id; }
              );
              if (item_to_remove) {
                var updated_item_offers = offer.items.filter(
                  function (row_id) { return row_id != item_to_remove.posa_row_id; }
                );
                offer.items = updated_item_offers;
                this$1.remove_item(item_to_remove);
                existOffer.give_item_row_id = null;
                existOffer.give_item = null;
              }
              var newItemOffer = this$1.ApplyOnGiveProduct(offer);
              if (offer.replace_cheapest_item) {
                var cheapestItem = this$1.getCheapestItem(offer);
                var oldBaseItem = this$1.items.find(
                  function (el) { return el.posa_row_id == item_to_remove.posa_is_replace; }
                );
                newItemOffer.qty = item_to_remove.qty;
                if (oldBaseItem && !oldBaseItem.posa_is_replace) {
                  oldBaseItem.qty += item_to_remove.qty;
                } else {
                  var restoredItem = this$1.ApplyOnGiveProduct(
                    {
                      given_qty: item_to_remove.qty,
                    },
                    item_to_remove.item_code
                  );
                  restoredItem.posa_is_offer = 0;
                  this$1.items.unshift(restoredItem);
                }
                newItemOffer.posa_is_offer = 0;
                newItemOffer.posa_is_replace = cheapestItem.posa_row_id;
                var diffQty = cheapestItem.qty - newItemOffer.qty;
                if (diffQty <= 0) {
                  newItemOffer.qty += diffQty;
                  this$1.remove_item(cheapestItem);
                  newItemOffer.posa_row_id = cheapestItem.posa_row_id;
                  newItemOffer.posa_is_replace = newItemOffer.posa_row_id;
                } else {
                  cheapestItem.qty = diffQty;
                }
              }
              this$1.items.unshift(newItemOffer);
              existOffer.give_item_row_id = newItemOffer.posa_row_id;
              existOffer.give_item = newItemOffer.item_code;
            } else if (
              existOffer.offer === 'Give Product' &&
              existOffer.give_item &&
              existOffer.give_item == offer.give_item &&
              (offer.replace_item || offer.replace_cheapest_item)
            ) {
              this$1.$nextTick(function () {
                var this$1 = this;

                var offerItem = this.getItemFromRowID(
                  existOffer.give_item_row_id
                );
                var diff = offer.given_qty - offerItem.qty;
                if (diff > 0) {
                  var itemsRowID = JSON.parse(existOffer.items);
                  var itemsList = [];
                  itemsRowID.forEach(function (row_id) {
                    itemsList.push(this$1.getItemFromRowID(row_id));
                  });
                  var existItem = itemsList.find(
                    function (el) { return el.item_code == offerItem.item_code &&
                      el.posa_is_replace != offerItem.posa_row_id; }
                  );
                  if (existItem) {
                    var diffExistQty = existItem.qty - diff;
                    if (diffExistQty > 0) {
                      offerItem.qty += diff;
                      existItem.qty -= diff;
                    } else {
                      offerItem.qty += existItem.qty;
                      this.remove_item(existItem);
                    }
                  }
                }
              });
            } else if (existOffer.offer === 'Item Price') {
              this$1.ApplyOnPrice(offer);
            } else if (existOffer.offer === 'Grand Total') {
              this$1.ApplyOnTotal(offer);
            }
            this$1.addOfferToItems(existOffer);
          } else {
            this$1.applyNewOffer(offer);
          }
        });
      },

    removeApplyOffer: function removeApplyOffer(invoiceOffer) {
        if (invoiceOffer.offer === 'Item Price') {
          this.RemoveOnPrice(invoiceOffer);
          var index = this.posa_offers.findIndex(
            function (el) { return el.row_id === invoiceOffer.row_id; }
          );
          this.posa_offers.splice(index, 1);
        }
        if (invoiceOffer.offer === 'Give Product') {
          var item_to_remove = this.items.find(
            function (item) { return item.posa_row_id == invoiceOffer.give_item_row_id; }
          );
          var index$1 = this.posa_offers.findIndex(
            function (el) { return el.row_id === invoiceOffer.row_id; }
          );
          this.posa_offers.splice(index$1, 1);
          this.remove_item(item_to_remove);
        }
        if (invoiceOffer.offer === 'Grand Total') {
          this.RemoveOnTotal(invoiceOffer);
          var index$2 = this.posa_offers.findIndex(
            function (el) { return el.row_id === invoiceOffer.row_id; }
          );
          this.posa_offers.splice(index$2, 1);
        }
        if (invoiceOffer.offer === 'Loyalty Point') {
          var index$3 = this.posa_offers.findIndex(
            function (el) { return el.row_id === invoiceOffer.row_id; }
          );
          this.posa_offers.splice(index$3, 1);
        }
        this.deleteOfferFromItems(invoiceOffer);
      },

     applyNewOffer: function applyNewOffer(offer) {
        var this$1 = this;

        if (offer.offer === 'Item Price') {
          this.ApplyOnPrice(offer);
        }
        if (offer.offer === 'Give Product') {
          var itemsRowID;
          if (typeof offer.items === 'string') {
            itemsRowID = JSON.parse(offer.items);
          } else {
            itemsRowID = offer.items;
          }
          if (
            offer.apply_on == 'Item Code' &&
            offer.apply_type == 'Item Code' &&
            offer.replace_item
          ) {
            var item = this.ApplyOnGiveProduct(offer, offer.item);
            item.posa_is_replace = itemsRowID[0];
            var baseItem = this.items.find(
              function (el) { return el.posa_row_id == item.posa_is_replace; }
            );
            var diffQty = baseItem.qty - offer.given_qty;
            item.posa_is_offer = 0;
            if (diffQty <= 0) {
              item.qty = baseItem.qty;
              this.remove_item(baseItem);
              item.posa_row_id = item.posa_is_replace;
            } else {
              baseItem.qty = diffQty;
            }
            this.items.unshift(item);
            offer.give_item_row_id = item.posa_row_id;
          } else if (
            offer.apply_on == 'Item Group' &&
            offer.apply_type == 'Item Group' &&
            offer.replace_cheapest_item
          ) {
            var itemsList = [];
            itemsRowID.forEach(function (row_id) {
              itemsList.push(this$1.getItemFromRowID(row_id));
            });
            var baseItem$1 = itemsList.find(
              function (el) { return el.item_code == offer.give_item; }
            );
            var item$1 = this.ApplyOnGiveProduct(offer, offer.give_item);
            item$1.posa_is_offer = 0;
            item$1.posa_is_replace = baseItem$1.posa_row_id;
            var diffQty$1 = baseItem$1.qty - offer.given_qty;
            if (diffQty$1 <= 0) {
              item$1.qty = baseItem$1.qty;
              this.remove_item(baseItem$1);
              item$1.posa_row_id = item$1.posa_is_replace;
            } else {
              baseItem$1.qty = diffQty$1;
            }
            this.items.unshift(item$1);
            offer.give_item_row_id = item$1.posa_row_id;
          } else {
            var item$2 = this.ApplyOnGiveProduct(offer);
            this.items.unshift(item$2);
            if (item$2) {
              offer.give_item_row_id = item$2.posa_row_id;
            }
          }
        }
        if (offer.offer === 'Grand Total') {
          this.ApplyOnTotal(offer);
        }
        if (offer.offer === 'Loyalty Point') {
          evntBus.$emit('show_mesage', {
            text: __('Loyalty Point Offer Applied'),
            color: 'success',
          });
        }

        var newOffer = {
          offer_name: offer.name,
          row_id: offer.row_id,
          apply_on: offer.apply_on,
          offer: offer.offer,
          items: JSON.stringify(offer.items),
          give_item: offer.give_item,
          give_item_row_id: offer.give_item_row_id,
          offer_applied: offer.offer_applied,
          coupon_based: offer.coupon_based,
          coupon: offer.coupon,
        };
        this.posa_offers.push(newOffer);
        this.addOfferToItems(newOffer);
      },

     ApplyOnGiveProduct: function ApplyOnGiveProduct(offer, item_code) {
        if (!item_code) {
          item_code = offer.give_item;
        }
        var items = this.allItems;
        var item = items.find(function (item) { return item.item_code == item_code; });
        if (!item) {
          return;
        }
        var new_item = Object.assign({}, item);
        new_item.qty = offer.given_qty;
        new_item.stock_qty = offer.given_qty;
        new_item.rate = offer.discount_type === 'Rate' ? offer.rate : item.rate;
        new_item.discount_amount =
          offer.discount_type === 'Discount Amount' ? offer.discount_amount : 0;
        new_item.discount_percentage =
          offer.discount_type === 'Discount Percentage'
            ? offer.discount_percentage
            : 0;
        new_item.discount_amount_per_item = 0;
        new_item.uom = item.uom ? item.uom : item.stock_uom;
        new_item.actual_batch_qty = '';
        new_item.conversion_factor = 1;
        new_item.posa_offers = JSON.stringify([]);
        new_item.posa_offer_applied = 0;
        new_item.posa_is_offer = 1;
        new_item.posa_is_replace = null;
        new_item.posa_notes = '';
        new_item.posa_delivery_date = '';
        new_item.is_free_item =
          (offer.discount_type === 'Rate' && !offer.rate) ||
          (offer.discount_type === 'Discount Percentage' &&
            offer.discount_percentage == 0)
            ? 1
            : 0;
        new_item.posa_row_id = this.makeid(20);
        new_item.price_list_rate =
          (offer.discount_type === 'Rate' && !offer.rate) ||
          (offer.discount_type === 'Discount Percentage' &&
            offer.discount_percentage == 0)
            ? 0
            : item.rate;
        if (
          (!this.pos_profile.posa_auto_set_batch && new_item.has_batch_no) ||
          new_item.has_serial_no
        ) {
          this.expanded.push(new_item);
        }
        this.update_item_detail(new_item);
        return new_item;
      },


     ApplyOnPrice: function ApplyOnPrice(offer) {
        var this$1 = this;

        this.items.forEach(function (item) {
          if (offer.items.includes(item.posa_row_id)) {
            var item_offers = JSON.parse(item.posa_offers);
            if (!item_offers.includes(offer.row_id)) {
              if (offer.discount_type === 'Rate') {
                item.rate = offer.rate;
              } else if (offer.discount_type === 'Discount Percentage') {
                item.discount_percentage += offer.discount_percentage;
              } else if (offer.discount_type === 'Discount Amount') {
                item.discount_amount += offer.discount_amount;
              }
              item.posa_offer_applied = 1;
              this$1.calc_item_price(item);
            }
          }
        });
      },

    RemoveOnPrice: function RemoveOnPrice(offer) {
        var this$1 = this;

        this.items.forEach(function (item) {
          var item_offers = JSON.parse(item.posa_offers);
          if (item_offers.includes(offer.row_id)) {
            var originalOffer = this$1.posOffers.find(
              function (el) { return el.name == offer.offer_name; }
            );
            if (originalOffer) {
              if (originalOffer.discount_type === 'Rate') {
                item.rate = item.price_list_rate;
              } else if (originalOffer.discount_type === 'Discount Percentage') {
                item.discount_percentage -= offer.discount_percentage;
                if (!item.discount_percentage) {
                  item.discount_percentage = 0;
                  item.discount_amount = 0;
                  item.rate = item.price_list_rate;
                }
              } else if (originalOffer.discount_type === 'Discount Amount') {
                item.discount_amount -= offer.discount_amount;
              }
              this$1.calc_item_price(item);
            }
          }
        });
      },

    
      ApplyOnTotal: function ApplyOnTotal(offer) {
        if (!offer.name) {
          offer = this.posOffers.find(function (el) { return el.name == offer.offer_name; });
        }
        if (
          (!this.discount_percentage_offer_name ||
            this.discount_percentage_offer_name == offer.name) &&
          offer.discount_percentage > 0 &&
          offer.discount_percentage <= 100
        ) {
          this.discount_amount = (
            (flt(this.Total) * flt(offer.discount_percentage)) /
            100
          ).toFixed(2);
          this.discount_percentage_offer_name = offer.name;
        }
      },

      RemoveOnTotal: function RemoveOnTotal(offer) {
        if (
          this.discount_percentage_offer_name &&
          this.discount_percentage_offer_name == offer.offer_name
        ) {
          this.discount_amount = 0;
          this.discount_percentage_offer_name = null;
        }
      },

    addOfferToItems: function addOfferToItems(offer) {
        var this$1 = this;

        var offer_items = JSON.parse(offer.items);
        offer_items.forEach(function (el) {
          this$1.items.forEach(function (exist_item) {
            if (exist_item.posa_row_id == el) {
              var item_offers = JSON.parse(exist_item.posa_offers);
              if (!item_offers.includes(offer.row_id)) {
                item_offers.push(offer.row_id);
                if (offer.offer === 'Item Price') {
                  exist_item.posa_offer_applied = 1;
                }
              }
              exist_item.posa_offers = JSON.stringify(item_offers);
            }
          });
        });
      },

    deleteOfferFromItems: function deleteOfferFromItems(offer) {
        var this$1 = this;

        var offer_items = JSON.parse(offer.items);
        offer_items.forEach(function (el) {
          this$1.items.forEach(function (exist_item) {
            if (exist_item.posa_row_id == el) {
              var item_offers = JSON.parse(exist_item.posa_offers);
              var updated_item_offers = item_offers.filter(
                function (row_id) { return row_id != offer.row_id; }
              );
              if (offer.offer === 'Item Price') {
                exist_item.posa_offer_applied = 0;
              }
              exist_item.posa_offers = JSON.stringify(updated_item_offers);
            }
          });
        });
      },

      validate_due_date: function validate_due_date(item) {
        var today = frappe.datetime.now_date();
        var parse_today = Date.parse(today);
        var new_date = Date.parse(item.posa_delivery_date);
        if (new_date < parse_today) {
          setTimeout(function () {
            item.posa_delivery_date = today;
          }, 0);
        }
      },
    },

  created: function created() {
      var this$1 = this;

      evntBus.$on('register_pos_profile', function (data) {
        this$1.pos_profile = data.pos_profile;
        this$1.customer = data.pos_profile.customer;
        this$1.pos_opening_shift = data.pos_opening_shift;
        this$1.stock_settings = data.stock_settings;
      });
     evntBus.$on('add_item', (item) => {
      // Customized By Thirvusoft
      // Start
      var ts_barcode=item.ts_matched_barcode
      var ts_item=item.item_code
      var out=this
      frappe.call({
        async:false,
        method:"posawesome.posawesome.api.posapp.batch_finder",
        args:{ts_barcode,
              ts_item},
        callback(ts_r){
          if(ts_r.message === 0){
            out.add_item(item);
          }
          if(typeof ts_r.message === 'string'){
            item["ts_current_batch"]=ts_r.message
            out.add_item(item);
          }else{
            if(ts_r.message.length>1){
              const ls=[]
              var ts_maping={}
            for (var i = 0; i < ts_r.message.length; i++) {
              ls.push("Batch No:- "+ts_r.message[i]["name"] +  " |MRP:- " + ts_r.message[i]["ts_mrp"])
              ts_maping["Batch No:- "+ts_r.message[i]["name"] +  " |MRP:- " + ts_r.message[i]["ts_mrp"]]=ts_r.message[i]["name"]
            }
              let d = new frappe.ui.Dialog({
              title: 'Batch Selection',
              fields: [               
                  {
                      label: 'Batch No',
                      fieldname: 'batch_no',
                      fieldtype: "Select",
                      options: ls
                  },
              ],
              primary_action_label: 'OK',
              primary_action(values) {
                  item["ts_current_batch"]=ts_maping[values["batch_no"]]
                  out.add_item(item);
                  d.hide();
                  evntBus.$emit('focus_on_search');
              }
          });
          d.show();
            }
            else{
              item["ts_current_batch"]=ts_r.message[0]["name"]
              out.add_item(item);
            }
          }
        }
      })
      // End
    });
      evntBus.$on('update_customer', function (customer) {
        this$1.customer = customer;
      });
      evntBus.$on('new_invoice', function () {
        this$1.invoice_doc = '';
        this$1.cancel_invoice();
      });
      evntBus.$on('load_invoice', function (data) {
        this$1.new_invoice(data);
        evntBus.$emit('set_pos_coupons', data.posa_coupons);
      });
      evntBus.$on('set_offers', function (data) {
        this$1.posOffers = data;
      });
      evntBus.$on('update_invoice_offers', function (data) {
        this$1.updateInvoiceOffers(data);
      });
      evntBus.$on('update_invoice_coupons', function (data) {
        this$1.posa_coupons = data;
        this$1.handelOffers();
      });
      evntBus.$on('set_all_items', function (data) {
        this$1.allItems = data;
        this$1.items.forEach(function (item) {
          this$1.update_item_detail(item);
        });
      });
      evntBus.$on('load_return_invoice', function (data) {
        this$1.new_invoice(data.invoice_doc);
        this$1.discount_amount = -data.return_doc.discount_amount;
        this$1.additional_discount_percentage =
          -data.return_doc.additional_discount_percentage;
        this$1.return_doc = data.return_doc;
      });
      document.addEventListener('keydown', this.shortOpenPayment.bind(this));
      document.addEventListener('keydown', this.shortDeleteFirstItem.bind(this));
      document.addEventListener('keydown', this.shortOpenFirstItem.bind(this));
      document.addEventListener('keydown', this.shortSelectDiscount.bind(this));
      // Customized By Thirvusoft
      // Start
      document.addEventListener('keydown', this.shortOpenReturn.bind(this));
      document.addEventListener('keydown', this.shortCancelInvoice.bind(this));
      // End
    },
    destroyed: function destroyed() {
      document.removeEventListener('keydown', this.shortOpenPayment);
      document.removeEventListener('keydown', this.shortDeleteFirstItem);
      document.removeEventListener('keydown', this.shortOpenFirstItem);
      document.removeEventListener('keydown', this.shortSelectDiscount);
      // Customized By Thirvusoft
      // Start
      document.removeEventListener('keydown', this.shortOpenReturn);
      document.addEventListener('keydown', this.shortCancelInvoice.bind(this));
      // End
    },
    watch: {
      customer: function customer() {
        this.close_payments();
        evntBus.$emit('set_customer', this.customer);
        this.fetch_customer_details();
      },
      customer_info: function customer_info() {
        evntBus.$emit('set_customer_info_to_edit', this.customer_info);
      },
      expanded: function expanded(data_value) {
        this.update_items_details(data_value);
        if (data_value.length > 0) {
          this.update_item_detail(data_value[0]);
        }
      },
      discount_percentage_offer_name: function discount_percentage_offer_name() {
        evntBus.$emit('update_discount_percentage_offer_name', {
          value: this.discount_percentage_offer_name,
        });
      },
      items: {
        deep: true,
        handler: function handler(items) {
          this.handelOffers();
          this.$forceUpdate();
        },
      },
      invoiceType: function invoiceType() {
        evntBus.$emit('update_invoice_type', this.invoiceType);
      },
      discount_amount: function discount_amount() {
        if (!this.discount_amount || this.discount_amount == 0) {
          this.additional_discount_percentage = 0;
        } else if (this.pos_profile.posa_use_percentage_discount) {
          this.additional_discount_percentage =
            (this.discount_amount / this.Total) * 100;
        } else {
          this.additional_discount_percentage = 0;
        }
      },
    },
  };
</script>

<style scoped>
.border_line_bottom {
  border-bottom: 1px solid lightgray;
}
.disable-events {
  pointer-events: none;
}
</style>
