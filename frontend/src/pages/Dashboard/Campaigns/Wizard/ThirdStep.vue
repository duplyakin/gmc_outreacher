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
                  v-model="timePickerFrom"
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
                  v-model="timePickerTill"
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
      selects: {
        simple: timezones.find(x => x.value === this.$store.state.campaign.timeTable.timezone).label,
        types: timezones,
        multiple: "ARS"
      },
      timePickerFrom: this.$store.state.campaign.timeTable.from,
      timePickerTill: this.$store.state.campaign.timeTable.till,
      model: {
        timePickerTill: ""
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
      tableData: this.$store.state.campaign.timeTable.days,
    };
  },
  methods: {
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    validate() {
      let data = {
        from: this.timePickerFrom,
        till: this.timePickerTill,
        timezone: this.selects.simple,
        days: this.tableData,
      };
      //console.log(data);
      this.$store.commit("step_3", data);

      return this.$validator.validateAll().then(res => {
        this.$emit("on-validated", res, this.model);
        return res;
      });
    }
  }
};
</script>
<style>
</style>
