<template>
     <div class="row">
        <div class="col-md-6">
            <EntriesForm
                :Riders= "AllRiders"
            />
        </div>
        <div class="col-md-6">
            <EntriesToday              
               
            />
        </div>
    </div>
   
</template>

<script>
import EntriesToday from '../components/EntriesToday.vue'
import EntriesForm from '../components/EntriesForm.vue'
import { computed } from '@vue/reactivity'
import { GetRiders } from '../../graphql'

export default {
    name: 'CreateEntries',
    components: { EntriesToday, EntriesForm },

    setup() {
         const AllRiders = computed(() => GetRiders.value)         
         console.log(AllRiders.value)

          return {
            AllRiders,
        }
    },
}
</script>

<style scoped>

</style>