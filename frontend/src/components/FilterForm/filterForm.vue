<template>
        <card>
            <template slot="header">
                <h4 class="card-title">{{ formTitle }}</h4>
            </template>
            <div>
            <form method="get" action="/" class="form-horizontal">
                <div v-for="i in 3">
                <o-filter filter_title="i"></o-filter> 
                </div>
            </form>

            <div class="row">
                    <button type="button" class="btn btn-wd btn-danger">Clear Filter</button>
                    <button type="button" class="btn btn-wd btn-success">Save Filter</button>
                    <button type="submit" class="btn btn-wd btn-success">Apply Filter</button>
            </div>
            
            </div>
        </card>
    </template>

<script>
import OFilter from 'src/components/FilterForm/filter.vue'

export default {
    components: {
        OFilter
    },
    name : 'filter-form',
    props: ['formTitle'],
    data () {
        return {
            
        }
    }
}
</script>
<style>
</style>
      