<template>
  <div>
    <h5 class="text-center">Preview & Start</h5>
    <card>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign name</p>here data...
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign type</p>here data...
        </h5>
      </div>
    </card>
  </div>
</template>
<script>
import { mapFields } from "vee-validate";
import { Select, Option } from "element-ui";

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option
  },
  computed: {
    ...mapFields(["website", "language", "bootstrapVersion"])
  },
  data() {
    return {
      model: {},
      modelValidations: {
        website: {
          url: true,
          required: true
        }
      }
    };
  },
  methods: {
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    validate() {
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
