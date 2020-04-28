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
                  v-model="model.timeTable.from"
                  v-validate="modelValidations.timePickerFrom"
                  :picker-options="{
                  start: '00:00',
                  step: '00:15',
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
                  v-model="model.timeTable.till"
                  v-validate="modelValidations.timePickerTill"
                  :picker-options="{
                  start: '00:00',
                  step: '00:15',
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
      <div class="row table-full-width">
        <div class="col-12">
          <el-table class="table-striped" :data="tableData">
            <el-table-column type="index"></el-table-column>
            <el-table-column prop="day"></el-table-column>
            <el-table-column label="Day">
              <template slot-scope="props">
                <l-switch v-model="props.row.active"></l-switch>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { Table, TableColumn, TimeSelect, Select, Option } from "element-ui";
import LSwitch from "src/components/Switch.vue";
import timezones from "./timezone";
export default {
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
      model: {
        timeTable: {
          from: '',
          till: '',
          timezone: '',
          days: this.tableData,
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
      //tableData: this.campaign.timeTable.days,
      tableData: [
            {
              day: "Sun",
              active: false
            },
            {
              day: "Mon",
              active: true
            },
            {
              day: "Tue",
              active: true
            },
            {
              day: "Wed",
              active: true
            },
            {
              day: "Thu",
              active: true
            },
            {
              day: "Fri",
              active: true
            },
            {
              day: "Sat",
              active: false
            }
          ],
    };
  },
  methods: {
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    validate() {
      return this.$validator.validateAll().then(res => {
          if(res) {
            this.model.timeTable.timezone = this.selects.simple,
            this.model.timeTable.days = this.tableData,
            this.$emit("on-validated", 'step_3', res, this.model);
          };
          return res;
        });
    }
  }
};
</script>
<style>
</style>
