<template>
  <div>
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
  Option
} from "element-ui";
import { PulseLoader } from 'vue-spinner/dist/vue-spinner.min.js'
export default {
  components: {
    PulseLoader,
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
    }, 5000);
  }
};
</script>

<style>
body {
  margin: 0;
}
</style>