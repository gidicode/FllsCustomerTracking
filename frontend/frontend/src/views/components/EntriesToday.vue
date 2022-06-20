<template >    
    <div class="container-fluid">
        <div class="input-group">
            <span 
                class="input-group-text icon" id="basic-addon1"><i class="fas fa-search text-white"></i></span>                     
            <input type="text" v-model="searchName" class="form-control" placeholder="Search..." aria-describedby="basic-addon1"/>
            <span class="clear btn btn-outline-dark" @click="clearSearch()">
                <i class="fas fa-times"></i></span>            
        </div>

        <div v-if="searchName.length > 0" class="mt-4">           
            <div v-if="load" class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>    

            <div 
                class="d-flex 
                    flex-row 
                    bd-highlight 
                    justify-content-around" 
                    v-for="i in searchedCustomers" 
                    :key="i.id"
                >
                <div class="p-2 bd-highlight flex-fill">{{ i.customerName }}</div>
                <div class="p-2 bd-highlight ">{{ i.customerContact }}</div>
                <div class="p-2 bd-highlight  ">
                    <span 
                        @click="pushNumber(i.customerContact)"
                         class="btn btn-sm btn-outline-success">
                         Add
                    </span>
                </div>
            </div>              
        </div>                      
        
    </div>                    
</template>

<script>
import { computed, ref } from '@vue/reactivity'
import { RecordQueryUnique, load } from '../../graphql'
import { useStore } from 'vuex'

export default {
    name: 'EntriesToday',    
    setup() {
        const store = useStore()       
        const uniqueCustomers = computed(() => RecordQueryUnique.value)                

        const searchName = ref('')
        
        const searchedCustomers = computed(() => {            
            return uniqueCustomers.value.filter((allCustomer) => {                
                return (                    
                    allCustomer.customerName
                    .toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1 ||
                    allCustomer.customerContact
                    .toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1
                )  
            }) 
        })

        const clearSearch = () => searchName.value = ''

        const pushNumber = (item) => {
            store.commit('pushNumber', item)
        }         
       

        return {
            uniqueCustomers,
            searchName, 
            searchedCustomers,
            clearSearch,
            pushNumber,                                
            load
        }
    },
}
</script>

<style scoped>
    .changeText {
        font-size: 14px;
    }

    .title{
        background-color: rgb(207, 238, 177);
        padding: 5px;
        border-radius: 10px;        
        font-weight: 500;
    }

    h6 {
        font-family: 'Comfortaa', cursive;
    }

</style> 