<template>
        <card>
            <filter-form formTitle="Test From"></filter-form>
        </card>
    </template>
    
<script>
    import FilterForm  from 'src/components/FilterForm/filterForm.vue'

    export default {
        components: {
            FilterForm
        },
        methods:{
        },
        data () {
            return {
                hello: "Hello world"
            }
        }
    }
</script>
<style>
</style>
    