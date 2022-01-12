<template>
    <div class="row">
        <div class="col-md-8">
            <recordList
                :uniqueCustomers = "uniqueCustomers"
                :multipleCustomers = "multipleCustomers"
            />            
        </div>
        <div class="col-md-3">
            <RecordDetails/>            
        </div>
    </div>
</template>

<script>
import  recordList from '../components/Records/RecordsList.vue'
import  RecordDetails from '../components/Records/RecordsDetails.vue'
import { RecordQueryUnique, RecordQueryMultiple } from '../../graphql'
import { computed } from '@vue/reactivity'

export default {
    name: "Records",
    components: {
        recordList,
        RecordDetails
    },   

    setup() {

        const uniqueCustomers = computed(() => RecordQueryUnique.value)
        const multipleCustomers = computed(() => RecordQueryMultiple.value)        
        
        return {
            uniqueCustomers,
            multipleCustomers,
            recordList,
            RecordDetails
        }
    },
}
</script>