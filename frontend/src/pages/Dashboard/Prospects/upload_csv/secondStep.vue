<template>
<div>
    <h5 class="text-center">Select file and map fields</h5>
    <div v-if="error" class="text-center text-danger invalid-feedback" style="display: block;">
            {{ error_message }}
    </div>
    <card>

    <div class="row">
    <div class="col-12">
        <vue-csv-import class="vue-csv-import" width="100%" v-model="model.file" :map-fields="model.map_fields">                 
                <template slot="hasHeaders" slot-scope="{headers, toggle}">
                        <label for="hasHeaders" class="form-check-label">
                            <input id="hasHeaders" type="checkbox" class="form-check-input" :value="headers" @change="toggle">
                            <span class="form-check-sign"></span>File has headers
                        </label>
                    </template>
                                  
                    <template slot="thead">
                        <tr>
                            <th>My Fields</th>
                            <th>Column</th>
                        </tr>
                    </template>
                 
                    <template slot="next" slot-scope="{load}">
                        <button class="btn btn-fill btn-info" @click.prevent="load">Map fields</button>
                    </template>
                 
                    <template slot="submit" slot-scope="{submit}">
                        <button @click.prevent="submit">send!</button>
                    </template>
                
        </vue-csv-import>
    </div>
    </div>
</card>
</div>
</template>
<script>
import { VueCsvImport } from 'vue-csv-import';

export default {
    name : 'second-step',
    components: {
        VueCsvImport
    },
    data () {
    return {
        model :{
            file : '',
            map_fields: []
        },
        error: false,
        error_message : 'File required',
    }
    },
    methods: {
    getError (fieldName) {
        return this.errors.first(fieldName)
    },
    validate () {
        return this.$validator.validateAll().then(res => {
        this.$emit('on-validated', res, this.model)
        return res
        })
    }
    },
    mounted() {
    }
}
</script>
<style>
</style>
