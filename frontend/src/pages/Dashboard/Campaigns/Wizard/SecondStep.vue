<template>
  <div>
    <div v-if="email_data.templates.length != 0" class="row">
      <div class="col-12">
        <card title="Email templates required">
          <el-table
            stripe
            ref="email_templates_data_table"
            style="width: 100%;"
            :data="email_data.templates"
            max-height="500"
            border
          >
            <el-table-column
              v-for="(column, index) in email_data.table_columns"
              :key="index"
              :label="column.label"
              :prop="column.prop"
              show-overflow-tooltip
            >
              <template slot-scope="scope">
                <a
                  @click.prevent="editEmailTemplate(scope.row, scope.$index)"
                  href="#"
                  v-if="column.prop === 'title'"
                >{{ scope.row[column.prop] }}</a>
                <template v-else>{{ scope.row[column.prop] }}</template>
              </template>
            </el-table-column>
          </el-table>
        </card>
      </div>
    </div>

    <div v-if="linkedin_data.templates.length != 0" class="row">
      <div class="col-12">
        <card title="Linkedin templates required">
          <el-table
            stripe
            ref="linkedin_templates_data_table"
            style="width: 100%;"
            :data="linkedin_data.templates"
            max-height="500"
            border
          >
            <el-table-column
              v-for="(column, index) in linkedin_data.table_columns"
              :key="index"
              :label="column.label"
              :prop="column.prop"
              show-overflow-tooltip
            >
              <template slot-scope="scope">
                <a
                  @click.prevent="editLinkedinTemplate(scope.row, scope.$index)"
                  href="#"
                  v-if="column.prop === 'title'"
                >{{ scope.row[column.prop] }}</a>
                <template v-else>{{ scope.row[column.prop] }}</template>
              </template>
            </el-table-column>
          </el-table>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
import { Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";
import MessageEdit from "./messageEdit.vue";
import NotificationMessage from "./notification.vue";

export default {
  props: {
    campaign: {
      templates: {
        email: Array,
        linkedin: Array
      }
    },
    email_data: Object,
    linkedin_data: Object
  },
  components: {
    MessageEdit,
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  data() {
    return {
      model: {
        email_templates: [],
        linkedin_templates: [],
      },
    };
  },
  methods: {
    editLinkedinTemplate(teamplateObj, row_index) {
      var table = this.$refs["linkedin_templates_data_table"];
      this.editTemplate("linkedin", teamplateObj, row_index, table);
    },
    editEmailTemplate(teamplateObj, row_index) {
      var table = this.$refs["email_templates_data_table"];
      this.editTemplate("email", teamplateObj, row_index, table);
    },
    editTemplate(template_type, templateObj, _row_index, _table) {
      const current_index = _row_index;
      const cuurent_table = _table;

      this.$modal.show(MessageEdit,
        {
          templateObj: templateObj,
          template_type: template_type,
          valueUpdated: newValue => {
            if (template_type === "email") {
              this.$set(this.email_data.templates, current_index, newValue);
            } else if (template_type === "linkedin") {
              this.$set(this.linkedin_data.templates, current_index, newValue);
            } else {
              alert("Unsupported template_type");
            }

            cuurent_table.$forceUpdate();
          }
        },
        {
          width: "720",
          height: "auto"
        }
      );
    },
    handleTest(index, row) {
      alert(`Your want to spaam-test ${row.name}`);
    },
    handleDelete(index, row) {
      //let indexToDelete = this.tableData.findIndex((tableRow) => tableRow.id === row.id)
      let indexToDelete = this.messages_data.messages.findIndex(
        tableRow => tableRow.id === row.id
      );
      //console.log("arr:", indexToDelete);
      if (indexToDelete >= 0) {
        //this.tableData.splice(indexToDelete, 1)
        this.messages_data.messages.splice(indexToDelete, 1);
      }
    },
    update_messages_data(newData) {
      if (newData.body && newData.subject) {
        var i = this.messages_data.messages.length;
        this.$set(this.messages_data.messages, i, newData);
      }
      //this.messages_data.pagination = JSON.parse(newData.pagination);
    },
    addMessage() {
      const _table = this.$refs.messages_data_table;
      this.$modal.show(
        MessageEdit,
        {
          messageObj: {},
          //modalTitle: "Prospect create",
          //action: 'create',
          //api_url : PROSPECTS_API_CREATE,
          valueUpdated: newValue => {
            this.$notify({
              component: NotificationMessage,
              message: "Message created Success",
              icon: "nc-icon nc-bulb-63",
              type: "success"
            });
            this.update_messages_data(newValue);
          }
        },
        {
          width: "720",
          height: "auto"
        }
      );
    },
    editMessage(msg_dict, row_index) {
      const current_index = row_index;
      const _table = this.$refs.messages_data_table;

      this.$modal.show(
        MessageEdit,
        {
          messageObj: msg_dict,
          //api_url : 'PROSPECTS_API_EDIT',
          //action: 'edit',
          //modalTitle: "Message edit",
          valueUpdated: newValue => {
            this.$set(this.messages_data.messages, current_index, newValue);
            _table.$forceUpdate();
            this.$notify({
              component: NotificationMessage,
              message: "Updated Success",
              icon: "nc-icon nc-bulb-63",
              type: "success"
            });
          }
        },
        {
          width: "720",
          height: "auto"
        }
      );
    },
    validate() {
      return this.$validator.validateAll().then(res => {
        if (res) {
          this.model.email_templates = this.email_data.templates;
          this.model.linkedin_templates = this.linkedin_data.templates;
          this.$emit("on-validated", "step_2_email", res, this.model);
        }
        return res;
      });
    }
  },
};
</script>
<style>
</style>
