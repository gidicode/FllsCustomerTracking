<template>
    <div class="row">
        <div class="col-md-4">
            <div class="back-ground shadow">
                <h5>All Riders </h5>
                <ul v-for="items in allRiders" :key="items.id">                                   
                    <li 
                        @click="sendRidersId(items.id)" 
                        v-if="items.id == getRiderInStore"
                        class="text-primary">
                            {{ items.riderName }}
                    </li>                                                                             
                    <li @click="sendRidersId(items.id)" v-else>{{ items.riderName }}</li>                                                                             
                </ul>
            </div>
        </div>
        <div class="col-md-2"></div>
        <div class="col-md-6">            
              <RidersDetails
                :allRiders='allRiders'
              />
        </div>
    </div>
</template>


<script>
import { computed } from '@vue/reactivity'
import { useStore } from 'vuex'
import RidersDetails from '../components/RidersDetails.vue'

import { GetRiders } from '../../graphql'
export default {
    name: 'Riders',
    components: {
        RidersDetails
    },
    setup() {
        const store = useStore()
        const allRiders = computed(() => GetRiders.value)        
        const getRiderInStore = computed(() => store.state.ridersId)

        const sendRidersId = (id) => {
            store.commit('updateRidersId', id)
            store.commit('openShowRidersDetails')
        }
        
        return {
            allRiders,            
            sendRidersId,
            RidersDetails,
            getRiderInStore,            
        }
    },
}
</script>

<style scoped>
.back-ground{
    background-color: rgb(255, 255, 255);
    padding: 20px;    
    height: 100vh;
    overflow: scroll;
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
    color: rgb(139, 166, 255);
}
</style>