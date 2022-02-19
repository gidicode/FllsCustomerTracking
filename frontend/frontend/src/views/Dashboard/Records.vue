<template>
<div>
    <div class="d-flex justify-content-center" v-if="load">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <div class="row" v-else>
        <div class="col-md-12">
            <recordList
                :uniqueCustomers = "uniqueCustomers"
                :multipleCustomers = "multipleCustomers"
            />            
        </div>       
    </div>
</div>
</template>

<script>
import  recordList from '../components/Records/RecordsList.vue'
import { RecordQueryUnique, RecordQueryMultiple, load } from '../../graphql'
import { computed } from '@vue/reactivity'

export default {
    name: "Records",
    components: {
        recordList,        
    },   

    setup() {
        const uniqueCustomers = computed(() => RecordQueryUnique.value)
        const multipleCustomers = computed(() => RecordQueryMultiple.value)                
        
        return {
            uniqueCustomers,
            multipleCustomers,
            recordList,     
            load                   
        }
    },
}
</script>

<style scoped>

</style>