<template>
  <div>
      <card>
        <h5 class="text-center">Let's create campaign!</h5>
        <div class="row">
          <div class="col-6">
            <fg-input
              :disabled="!list_data.modified_fields['title']"
              label="Campaign title"
              name="Campaign title"
              v-validate="modelValidations.campaignTitle"
              v-model="campaign.title"
              :error="getError('Campaign title')"
              placeholder="ex: My email campaign"
            ></fg-input>
          </div>
        </div>
      </card>
      <card>
        <div class="row">
          <div class="col-6">
            <p>Campaign funnel</p>
              <el-select
                class="select-default mb-3"
                name="Campaign funnel"
                v-on:change="onChangeFunnel"
                style="width: 100%;"
                placeholder="Select funnel"
                v-model="campaign.funnel"
                v-validate="modelValidations.campaignFunnel"
                value-key="title">
                <el-option
                  class="select-default"
                  v-for="(funnel,index) in list_data.funnels"
                  :key="funnel._id.$oid"
                  :label="funnel.title"
                  :value="funnel"
                ></el-option>
              </el-select>
            </fg-input>
          </div>
        </div>
      </card>

      <card>
        <div class="row">
          <div class="col-12">
            <card title="Select accounts based on medium (Linkedin or email)">
              <div v-if="hasMedium('email')" class="col-6">
                <p>Select Email account</p>
                <el-select
                  class="select-default mb-3"
                  style="width: 100%;"
                  placeholder="Select email account"
                  v-model="email_data.email_account_selected"
                  value-key="data.account"
                  v-validate="modelValidations.account"
                  :disabled="!list_data.modified_fields['credentials']"
                >
                  <el-option
                    class="select-default"
                    v-for="(account,index) in list_data.credentials"
                    v-if="account.medium == 'email'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account"
                  ></el-option>
                </el-select>
              </div>
              <div v-if="hasMedium('linkedin')" class="col-6">
                <p>Select Linkedin account</p>
                <el-select
                  class="select-default mb-3"
                  style="width: 100%;"
                  placeholder="Select linkedin account"
                  v-model="linkedin_data.linkedin_account_selected"
                  value-key="data.account"
                  v-validate="modelValidations.account"
                  :disabled="!list_data.modified_fields['credentials']"
                >
                  <el-option
                    class="select-default"
                    v-for="(account,index) in list_data.credentials"
                    v-if="account.medium == 'linkedin'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account"
                  ></el-option>
                </el-select>
              </div>
            </card>
          </div>
        </div>
      </card>
      <card>
        <div class="row">
          <div class="col-12">
            <card title="Select prospects list">
              <p>Select prospects list</p>
              <el-select
                class="select-default mb-3"
                style="width: 100%;"
                placeholder="Select prospects list"
                v-model="campaign.prospects_list"
                value-key="campaign.prospects_list"
                :disabled="!list_data.modified_fields['prospects_list']"
              >
                <el-option
                  class="select-default"
                  v-for="(list,index) in list_data.prospects_list"
                  :key="list._id.$oid"
                  :label="list.title"
                  :value="list"
                ></el-option>
              </el-select>
            </card>
          </div>
        </div>
      </card>

      <card v-if="list_data.modified_fields['templates'] && email_data.templates.length != 0">
        <div class="row">
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
      </card>

      <card v-if="list_data.modified_fields['templates'] && linkedin_data.templates.length != 0">
        <div class="row">
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
      </card>

      <card>
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
                      v-model="campaign.from_hour"
                      v-validate="modelValidations.timePickerFrom"
                      :disabled="!list_data.modified_fields['time_table']"
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
                      v-model="campaign.to_hour"
                      v-validate="modelValidations.timePickerTill"
                      :disabled="!list_data.modified_fields['time_table']"
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
                    v-model="timezones_selected"
                    v-validate="modelValidations.timeZone"
                    :disabled="!list_data.modified_fields['time_table']"
                  >
                    <el-option
                      v-for="option in timezones_selects"
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
                <button
                  type="button"
                  ref="day_0"
                  @click="toggleDay('day_0')"
                  :disabled="!list_data.modified_fields['time_table']"
                  v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign.sending_days['0'] }"
                >Mon</button>
                <button
                  type="button"
                  ref="day_1"
                  @click="toggleDay('day_1')"
                  :disabled="!list_data.modified_fields['time_table']"
                  v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign.sending_days['1'] }"
                >Tue</button>
                <button
                  type="button"
                  ref="day_2"
                  @click="toggleDay('day_2')"
                  :disabled="!list_data.modified_fields['time_table']"
                  v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign.sending_days['2'] }"
                >Wed</button>
                <button
                  type="button"
                  ref="day_3"
                  @click="toggleDay('day_3')"
                  :disabled="!list_data.modified_fields['time_table']"
                  v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign.sending_days['3'] }"
                >Thu</button>
                <button
                  type="button"
                  ref="day_4"
                  @click="toggleDay('day_4')"
                  :disabled="!list_data.modified_fields['time_table']"
                  v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign.sending_days['4'] }"
                >Fri</button>
                <button
                  type="button"
                  ref="day_5"
                  @click="toggleDay('day_5')"
                  :disabled="!list_data.modified_fields['time_table']"
                  v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign.sending_days['5'] }"
                >Sat</button>
                <button
                  type="button"
                  ref="day_6"
                  @click="toggleDay('day_6')"
                  :disabled="!list_data.modified_fields['time_table']"
                  v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign.sending_days['6'] }"
                >Sun</button>
              </div>
            </card>
          </div>
        </div>
      </card>

      <div class="col-8 d-flex flex-row-reverse align-self-center">
        <div>
          <button
            @click.prevent="preview()"
            type="button"
            class="btn btn-default btn-success mx-1"
          >Submit</button>
        </div>
      </div>

  </div>
</template>
<script>
import {
  Table,
  TableColumn,
  Input,
  Button,
  Select,
  Option,
  TimeSelect
} from "element-ui";
import swal from "sweetalert2";
import axios from '@/api/axios-auth';;
import MessageEdit from "./Wizard/messageEdit.vue";
import Preview from "./Preview.vue";
import timezones from "./Wizard/timezone";

const CAMPAIGNS_API_DATA = "http://127.0.0.1:5000/campaigns/data";
const CAMPAIGNS_API_CREATE = "http://127.0.0.1:5000/campaigns/create";
const CAMPAIGNS_API_GET_BY_ID = "http://127.0.0.1:5000/campaigns/get";

export default {
  components: {
    MessageEdit,
    [Input.name]: Input,
    [Button.name]: Button,
    [Option.name]: Option,
    [Select.name]: Select,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    [TimeSelect.name]: TimeSelect
  },
  data() {
    return {
      action_type: '', // 'edit' or 'add'
      campaign_id: '',

      timezones_selects: timezones,
      timezones_selected: "",

      list_data: {
        credentials: [],
        prospects_list: [],
        funnels: [],
        columns: [],
        modified_fields: {},
      },

      email_data: {
        email_account_selected: "",
        templates: [],
        table_columns: [
          {
            prop: "title",
            label: "Template title",
            minWidth: 300
          },
          {
            prop: "subject",
            label: "Subject",
            minWidth: 300
          },
          {
            prop: "interval",
            label: "Interval",
            minWidth: 100
          }
        ]
      },

      linkedin_data: {
        linkedin_account_selected: "",
        templates: [],
        table_columns: [
          {
            prop: "title",
            label: "Template title",
            minWidth: 300
          },
          {
            prop: "interval",
            label: "Interval",
            minWidth: 100
          }
        ]
      },

      campaign: {
        title: "",
        funnel: {},
        credentials: [],
        prospects_list: {},
        templates: {
          email: [],
          linkedin: []
        },
        from_hour: "",
        to_hour: "",
        time_zone: "",
        sending_days: {
          "0": true,
          "1": true,
          "2": true,
          "3": true,
          "4": true,
          "5": false,
          "6": false
        }
      },
      modelValidations: {
        campaignTitle: {
          required: true,
          min: 5
        },
        campaignFunnel: {
          required: true
        },
        account: {
          required: true
        },
        prospects: {
          required: true
        },
        timePickerTill: {
          required: true
        },
        timePickerFrom: {
          required: true
        },
        timeZone: {
          required: true
        }
      }
    };
  },

  methods: {
    toggleDay(ref) {
      var btn = this.$refs[ref];
      if (!btn) {
        return false;
      }

      var index = ref.split("_")[1];

      this.campaign.sending_days[index] = !this.campaign.sending_days[index];
      return true;
    },
    hasMedium(medium) {
      var templates_required = this.campaign.funnel.templates_required || null;
      if (templates_required) {
        var email = templates_required.email || null;
        var linkedin = templates_required.linkedin || null;

        if (medium == "email") {
          if (email) {
            return true;
          } else {
            return false;
          }
        }

        if (medium == "linkedin") {
          if (linkedin) {
            return true;
          } else {
            return false;
          }
        }
      }

      return false;
    },
    onChangeFunnel() {
      /* update tempaltes based on selected funnel */
      /* clear all data first */
      this.email_data.templates = [];
      this.linkedin_data.templates = [];
      this.email_data.email_account_selected = '';
      this.linkedin_data.linkedin_account_selected = '';

      var templates_required = this.campaign.funnel.templates_required || null;
      if (templates_required) {
        var email = templates_required.email || null;
        if (email) {
          this.email_data.templates = Object.values(email);

          /*sort by order field*/
          this.email_data.templates.sort(function(first, second) {
            return first["order"] - second["order"];
          });
        }

        var linkedin = templates_required.linkedin || null;
        if (linkedin) {
          this.linkedin_data.templates = Object.values(linkedin);

          /*sort by order field*/
          this.linkedin_data.templates.sort(function(first, second) {
            return first["order"] - second["order"];
          });
        }
      }

      console.log("new onchangefunnel");
      console.log(this.campaign.funnel);
      console.log(this.email_data.templates);
      console.log(this.linkedin_data.templates);
    },
    initCampaign() {
      this.action_type = this.$route.query.type;
      //console.log('type: ', type);

      if (this.action_type == "edit") {
        this.campaign_id = this.$route.query.id;
        //console.log('id: ', id);

        this.get_campaign_by_id(this.campaign_id);
        console.log("campaign: ", this.campaign);
        this.timezones_selected = timezones.find(x => x.value === this.campaign.time_zone).label || "";
        this.email_data.templates = this.campaign.templates.email;
        this.linkedin_data.templates = this.campaign.templates.linkedin;
        console.log("email_data: ", this.email_data.templates);
      }
      if (this.action_type == "add") {
        this.newCampaign(1);
      }

      console.log("initCampaign: ", this.campaign);
    },
    async get_campaign_by_id(id) {
      /* SENDING TO SERVER HERE */
      var path = CAMPAIGNS_API_GET_BY_ID;
      var get_data = new FormData();
      get_data.append("_campaign_id", id);

      await axios
        .post(path, get_data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error getting campaign " + r.msg;
            alert(msg);
          } else {
            var updated = r.updated;
            this.campaign = JSON.parse(r.campaign);
            this.list_data.modified_fields = JSON.parse(r.modified_fields);
            console.log("res: ", this.campaign);
            console.log("modified_fields: ", this.list_data.modified_fields);
          }
        })
        .catch(error => {
          var msg = "Error getting campaign " + error;
          alert(msg);
        });
    },
    async newCampaign(page = 1) {
      const path = CAMPAIGNS_API_DATA;

      var data = new FormData();
      //data.append("_create", 1);
      //?
      data.append("_page", page);

      //console.log(data);
      await axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading campaigns " + r.msg;
            alert(msg);
          } else {
            this.update_data(r);
          }
        })
        .catch(error => {
          var msg = "Error loading campaigns " + error;
          alert(msg);
        });
    },
    update_data(newJson) {
      this.list_data.prospects_list = JSON.parse(newJson.prospects_list);
      this.list_data.columns = JSON.parse(newJson.columns);
      this.list_data.funnels = JSON.parse(newJson.funnels);
      this.list_data.credentials = JSON.parse(newJson.credentials);
      this.list_data.modified_fields = JSON.parse(newJson.modified_fields);

      /* This will help to prevent: JSON parse error in console */
      if (newJson.campaigns) {
        this.list_data.campaigns = JSON.parse(newJson.campaigns);
      }
      console.log("load from server: ", this.list_data);
    },
    preview() {
      this.campaign.time_zone = this.timezones_selected;
      this.$validator.validateAll().then(res => {
        if (res) {
          this.$modal.show(Preview,
            {
              modified_fields: this.list_data.modified_fields,
              campaign_id: this.campaign_id,
              action_type: this.action_type,
              campaign: this.campaign,
              email_data: this.email_data,
              linkedin_data: this.linkedin_data
            },
            {
              width: "720",
              height: "auto",
              scrollable: true
            }
          );
        }
        return res;
      });
    },
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

      this.$modal.show(
        MessageEdit,
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
          height: "auto",
          scrollable: true
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
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
  },
  created() {
    this.initCampaign();
  }
};
</script>
<style lang="scss">
</style>
