<template >    
    <div class="container-fluid">
        <h6 class="mb-4">Entries Tday</h6>
        <div class="row">
            <div class="col">
                <span class="title mb-2">Individual</span>  
                <p v-for="i in singleEntries" :key="i.id" class="changeText">                         
                    <strong>{{ i.customerName }} </strong> {{ i.customerContact }}
                </p> 
            </div>
            <div class="col">
                <span class="title mb-2" >Repeated</span>  
                <p v-for="i in multipleEntries" :key="i.id" class="changeText"> 
                            
                    <strong>{{ i.customer.customerName }} </strong> {{ i.customer.customerContact }}
                </p> 
            </div>
        </div>        
    </div>                    
</template>

<script>
import { computed } from '@vue/reactivity'
import { multipleEntriesToday, singleEntriesToday } from '../../graphql'

export default {
    name: 'EntriesToday',
    setup() {
        const singleEntries = computed(() => singleEntriesToday.value)
        const multipleEntries = computed(() => multipleEntriesToday.value)                
        //console.log(singleEntries.value, 'single')
        
        return {
            multipleEntries,
            singleEntries
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