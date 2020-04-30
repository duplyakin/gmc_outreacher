<template>
  <div>
    <h5 class="text-center">Delivery time with respect to prospect's timezone</h5>
    <div class="extended-forms">
      <card>
        <div class="col-12">
          <div class="row">
            <div class="col-lg-6">
              <h4 class="title">From</h4>
              <fg-input :error="getError('From time')">
                <el-time-select
                  name="From time"
                  v-model="from"
                  v-validate="modelValidations.timePickerFrom"
                  :picker-options="{
                  start: '00:00',
                  step: '01:00',
                  end: '23:59'
                }"
                  placeholder="Select time"
                ></el-time-select>
              </fg-input>
            </div>
            <div class="col-lg-6">
              <h4 class="title">Till</h4>
              <fg-input :error="getError('Till time has to be after FROM time')">
                <el-time-select
                  name="Till time has to be after FROM time"
                  v-model="till"
                  v-validate="modelValidations.timePickerTill"
                  :picker-options="{
                  start: '00:00',
                  step: '01:00',
                  end: '23:59'
                }"
                  placeholder="Select time"
                ></el-time-select>
              </fg-input>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-6">
            <h4 class="title">Fallback Time Zone</h4>
            <fg-input :error="getError('Fallback Time Zone')">
              <el-select
                class="select-primary"
                name="Fallback Time Zone"
                size="large"
                placeholder="Fallback Time Zone"
                v-model="selects.simple"
                v-validate="modelValidations.timeZone"
              >
                <el-option
                  v-for="option in selects.types"
                  class="select-primary"
                  :value="option.value"
                  :label="option.label"
                  :key="option.label"
                ></el-option>
              </el-select>
            </fg-input>
          </div>
        </div>
      </card>
    </div>
    <h4 class="title">Days Preference</h4>
    <div class="row">
        <div class="col-12">
          <card title="Select sending days">
            <div class="btn-group">
              <button type="button" ref='day_0' @click="toggleDay('day_0')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': model.timeTable.days_selected['0'] }">Mon</button>
              <button type="button" ref='day_1' @click="toggleDay('day_1')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': model.timeTable.days_selected['1'] }">Tue</button>
              <button type="button" ref='day_2' @click="toggleDay('day_2')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': model.timeTable.days_selected['2'] }">Wed</button>
              <button type="button" ref='day_3' @click="toggleDay('day_3')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': model.timeTable.days_selected['3'] }">Thu</button>
              <button type="button" ref='day_4' @click="toggleDay('day_4')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': model.timeTable.days_selected['4'] }">Fri</button>
              <button type="button" ref='day_5' @click="toggleDay('day_5')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': model.timeTable.days_selected['5'] }">Sat</button>
              <button type="button" ref='day_6' @click="toggleDay('day_6')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': model.timeTable.days_selected['6'] }">Sun</button>
            </div>
          </card>
        </div>
    </div>
  </div>
</template>
<script>
import { Table, TableColumn, TimeSelect, Select, Option } from "element-ui";
import LSwitch from "src/components/Switch.vue";
import timezones from "./timezone";
export default {
  props: {
    campaign: {
        timeTable: {
          from: Number,
          till: Number,
          timezone: String,
          days: Object,
        },
    },
  },
  components: {
    LSwitch,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    [TimeSelect.name]: TimeSelect,
    [Option.name]: Option,
    [Select.name]: Select
  },
  data() {
    return {
      from: '',
      till: '',
      model: {
        timeTable: {
          from: 0,
          till: 0,
          timezone: '',
          days_selected: {
          '0' : true,
          '1' : true,
          '2' : true, 
          '3' : true,
          '4' : true,
          '5' : false,
          '6' : false
          },
        },
      },
      selects: {
        //simple: timezones.find(x => x.value === this.campaign.timeTable.timezone).label,
        simple: '',
        types: timezones,
        multiple: "ARS"
      },
      modelValidations: {
        timePickerTill: {
          required: true
        },
        timePickerFrom: {
          required: true
        },
        timeZone: {
          required: true
        }
      },

    };
  },
  methods: {
    toggleDay(ref){
    var btn = this.$refs[ref];
    if (!btn){
      return false;
    }
    
    var index = ref.split('_')[1];
    
    this.model.timeTable.days_selected[index] = !this.model.timeTable.days_selected[index];    
    return true;
  },
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    validate() {
      return this.$validator.validateAll().then(res => {
          if(res) {
            this.model.timeTable.from = parseInt(this.from, 10);
            this.model.timeTable.till = parseInt(this.till, 10);
            this.model.timeTable.timezone = this.selects.simple;
            this.$emit("on-validated", 'step_3', res, this.model);
          };
          return res;
        });
    }
  },
  mounted () {
      this.$nextTick(function () {
        this.from = this.campaign.timeTable.from.toString();
        this.till = this.campaign.timeTable.till.toString();
        this.selects.simple = timezones.find(x => x.value === this.campaign.timeTable.timezone).label;
        this.model.timeTable.days_selected = this.campaign.timeTable.days;
      })
    },
};
</script>
<style>
</style>
