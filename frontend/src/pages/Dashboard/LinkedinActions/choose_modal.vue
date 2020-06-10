<template>
  <div class="test-modal">
    <card title="Where do you want your leads to come from?">
      <div>
        <div class="col-6">
          <el-select
            class="select-default mb-3"
            style="width: 100%;"
            placeholder="Source of leads"
            v-model="campaign_type"
            value-key="label"
          >
            <el-option
              class="select-default"
              v-for="curent_type in campaign_types"
              :key="curent_type.label"
              :label="curent_type.label"
              :value="curent_type"
            ></el-option>
          </el-select>
        </div>

        <div class="col-8">
          <p class="descriptions">{{ campaign_type.description }}</p>
        </div>

        <div class="col-12 d-flex flex-row-reverse">
          <button
            type="submit"
            v-on:click="submit"
            class="btn btn-outline btn-wd btn-success mx-1"
          >Create</button>
          <button
            v-on:click="discard"
            type="discard"
            class="btn btn-outline btn-wd btn-danger"
          >Discard</button>
        </div>
      </div>
    </card>
  </div>
</template>

<script>
import { Notification, Select, Option } from "element-ui";
import Editor from "@tinymce/tinymce-vue";

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    editor: Editor
  },
  data() {
    return {
      campaign_type: {},
      campaign_types: [
        { label: "Add Leads from Linkedin search URL", description: "Cut and paste a Linkedin search URL to add leads." },
        { label: "Add Leads for Linkedin profiles from CSV", description: "Import a list of LinkedIn profiles to enrich." }
      ],
    };
  },
  methods: {
    submit() {
      if (this.campaign_type.label === "Add Leads from Linkedin search URL") {
        this.$router.push({
          path: "linkedin_parsing"
        });
      } else if (this.campaign_type.label === "Add Leads for Linkedin profiles from CSV") {
        this.$router.push({
          path: "linkedin_enrichment_data"
        });
      }
      this.$emit("close");
    },
    discard() {
      this.$emit("close");
    }
  },
};
</script>
<style>
.descriptions {
  display: flex;
  align-items: flex-start;
  font-size: 15px;
  font-weight: 50;
  line-height: 20px;
  color: rgb(119, 119, 119);
}
</style>
  