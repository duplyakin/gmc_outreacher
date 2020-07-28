<template>
  <div>

    <el-input label="Subject"
              placeholder="Enter Subject 1111"
              name="Subject">
    </el-input>
    <pulse-loader :loading="loading" :color="color"></pulse-loader>
    <el-table v-if="!loading" :data="tableData" style="width: 100%">
      <el-table-column prop="date" label="Date" width="180"></el-table-column>
      <el-table-column prop="name" label="Name" width="180"></el-table-column>
      <el-table-column prop="address" label="Address"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import {
  Notification,
  Loading,
  Table,
  TableColumn,
  Select,
  Option, 
  Input
} from "element-ui";
import { PulseLoader } from 'vue-spinner/dist/vue-spinner.min.js'

//import MyComp from '@/components/Inputs/formGroupInput'

//import o24inner from '@/assets/sass/lbd/element/_o24_input.scss'

export default {
  components: {
    PulseLoader,
    [Input.name]: Input,
    [Loading.name]: Loading,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  data() {
    return {
      tableData: [
        {
          date: "2016-05-02",
          name: "John Smith",
          address: "No.1518,  Jinshajiang Road, Putuo District"
        },
        {
          date: "2016-05-04",
          name: "John Smith",
          address: "No.1518,  Jinshajiang Road, Putuo District"
        },
        {
          date: "2016-05-01",
          name: "John Smith",
          address: "No.1518,  Jinshajiang Road, Putuo District"
        }
      ],
      loading: true,
      color: "#a7a7ff",
    };
  },
  mounted() {
    setTimeout(() => {
      this.loading = false
    }, 1000);
  }
};
</script>

<style scoped lang="scss">
@import "~assets/sass/_o24_input";
</style>