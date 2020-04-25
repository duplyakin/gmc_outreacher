<template>
<div>
    <h5 class="text-center">Third  step</h5>
    <div class="row">
    <div class="col-12">
        Third step
    </div>
    </div>
</div>
</template>
<script>
export default {
    name : 'third-step',

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
