<template>
    <aside>        
        <button @click="sendCloseEvent()" type="button" class="btn-close btn-light close-button " aria-label="Close"></button>
        <div class="d-flex flex-column bd-highlight text-white mb-3">
            <div class="p-2 bd-highlight">
                <h4>{{ CustomerName }}</h4>
                <h6>Customer Number: <strong> {{ CustomerContact }}</strong> </h6>
                <h6> Current Use: <strong>{{ lastUse }}</strong> </h6>
                <h6> First Rider: <strong> {{ rider }} </strong></h6>
                <h6>Discount: <strong> N{{ discount }} </strong> </h6>
            </div>
            <div class="p-2 bd-highlight">                
                <div class="lastUsed" v-for="i in filterItems" :key="i.id">
                    <p class="mt-2 fw-bold" v-if="i.count == '' ">
                        Last Used: {{ dateRange(i.dateCreated) }}
                    </p>
                    <p class="mt-2 fw-bold" v-else v-for="items in i.count.slice(0,1)" :key="items.id"> 
                        Last Used: {{ dateRange(items.dateCreated) }}
                    </p>
                </div>
            </div>
            <div class="p-2 bd-highlight">
               <div class="details-section">
                    <table class="table text-white table-borderless table-sm">
                        <thead v-for="i in filterItems" :key="i.id">
                            <tr v-if="i.count == '' "> </tr>
                            <tr v-else>
                                <th scope="col">s/n</th>
                                <th scope="col">Date</th>
                                <th scope="col">Rider</th>                                
                                <th scope="col">Discount</th>                                
                            </tr>
                        </thead>
                        <tbody v-for="i in filterItems" :key="i.id">
                            <div v-if="i.count == '' ">
                                <p class="nothing">Nothing to see here</p>
                            </div>
                            <tr v-else v-for="(items, index) in i.count" :key="items.id">                                
                                <td scope="row">{{ index + 1}}</td>
                                <td> <small> {{ dateTime(items.dateCreated) }} </small> </td>                                                            
                                <td> <small> {{ items.Rider.riderName}} </small> </td>
                                <td> <small> {{ items.discountAmount}} </small> </td>                                
                            </tr>                           
                        </tbody>
                    </table>
               </div>
            </div>

            <div class="p-2 bd-highlight">
                 
                <p></p>
            </div>
        </div>      
    </aside>
</template>

<script>
import { computed, toRef, watch } from '@vue/runtime-core'
import { useRoute } from 'vue-router'

export default {
    name: "RecordDetails",    
    props: {
        uniqueCustomers: Object,
        dateTime: Object,
        dateRange: Object,
    },
    emits: ['closeDetails'],

    setup(props, context) {
        const route = useRoute() 
        const CustomerName = computed(() => route.params.customerName)
        const CustomerContact = computed(() => route.params.customerContact)
        const lastUse = computed(() => route.params.lastUse)
        const rider = computed(() => route.params.firstRider)
        const discount = computed(() => route.params.discount)
        const listDelivery = computed(() => route.params.listDelivery)               
        const getCustomerDetails = toRef(props, 'uniqueCustomers')
        const sendCloseEvent = () => {
            context.emit('closeDetails')
        }


        watch(
            () => route.params, 
            () => {
                filterItems                
            }
        )
        const filterItems = computed (() => getCustomerDetails.value.filter(getCustomers => getCustomers.id == route.params.id))
        

        return{
            CustomerName,
            CustomerContact,
            lastUse,
            rider,
            discount,        
            listDelivery,
            filterItems,
            sendCloseEvent
        }
    },
}
</script>

<style scoped>

aside{
    background-color: #517fbb;
    height: auto;
    border-radius: 10px;
    padding: 20px;
}

.lastUsed{
    background: #83E38C;
    border-radius: 10px;
    padding: 1px;
    box-shadow: 0px 4px 4px 0px #00000026;
    text-align: center;    
    margin-bottom: 20px;
}

.details-section{
    background-color: #254472;
    border-radius: 10px;
    padding: 20px;
    height: 20rem;
    overflow: scroll;        
}

a {
    text-decoration: none;
}


.close-button{
    position: absolute;
    left: 17.7rem;            
}

.nothing{
    font-weight: 900;
    font-size: 40px;
}

::-webkit-scrollbar{
    width: 7px;
}

::-webkit-scrollbar-track {
    border-radius: 20px;
}

::-webkit-scrollbar-thumb {
    background-color: rgb(233, 240, 255);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background-color: rgb(182, 215, 255);
}
</style>