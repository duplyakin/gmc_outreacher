<template>
<div>
    <h5 class="text-center">Upload .csv file with data</h5>
    <div class="row">
    <div class="col-12">
        <el-upload
            class="upload"
            drag
            action=""
            :on-preview=""
            :on-remove=""
            :file-list="fileList"
            accept=".csv">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
            <div class="el-upload__tip" slot="tip">
                    Your file must contain a column with header: email. The value of this column will be your prospects email address.
                    [Maximum Upload File Size: 5MB or 10,000 rows]
            </div>
          </el-upload>
         </div>
    </div>
</div>
</template>
<script>
export default {
    name : 'first-step',
    data () {
    return {
        model: {
        firstName: '',
        lastName: '',
        email: ''
        },
        modelValidations: {
        firstName: {
            min: 5
        },
        lastName: {
            min: 5
        },
        email: {
            required: true,
            email: true
        }
        }
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
    }
}
</script>
<style>
</style>
