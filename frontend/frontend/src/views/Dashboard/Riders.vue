<template>
    <div class="row">
        <div class="col-md-4">
            <div class="back-ground shadow">
                <h5>All Riders </h5>
                <ul v-for="items in allRiders" :key="items.id">                
                    <router-link :to="{name: 'RidersDetails', 
                            params:{
                                id: items.id,
                                name: items.riderName
                            }
                        }">
                        <li>{{ items.riderName }}</li>
                    </router-link>                                                            
                </ul>
            </div>
        </div>
        <div class="col-md-2">

        </div>
        <div class="col-md-6">
              <router-view/>
        </div>
    </div>
</template>


<script>
import { computed } from '@vue/reactivity'

import { GetRiders, RecordQueryMultiple } from '../../graphql'
export default {
    setup() {
        const allRiders = computed(() => GetRiders.value)                
        const allLogs = computed(() => RecordQueryMultiple.value )        
        const getQueryOfRider = computed(() => allRiders.value.filter(riders => riders == allLogs.value.Rider))
        
        return {
            allRiders,
            getQueryOfRider
        }
    },
}
</script>

<style scoped>
.back-ground{
    background-color: rgb(255, 255, 255);
    padding: 20px;
    border-radius: 20px;
}

a{
    text-decoration: none;
    color: black;
}

 a.router-link-exact-active {    
    color: rgb(37, 73, 190);    
    font-weight: bold;           
}

li:hover{
    background-color: rgb(236, 253, 255);
    padding: 8px;    
    width: max-content;
    border-radius: 5px;

}
</style>