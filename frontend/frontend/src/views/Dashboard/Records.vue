<template>
<div>
    <div class="row">
        <div class="col-md-12">
            <recordList
                :uniqueCustomers = "uniqueCustomers"
                :multipleCustomers = "multipleCustomers"
                :type="type"
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
        const type = "type"               
        return {
            uniqueCustomers,
            multipleCustomers,
            recordList,     
            load,
            type           
        }
    },
}
</script>

<style scoped>

</style>