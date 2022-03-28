<template>
    <aside class="shadow-sm">        
        <button @click="sendCloseEvent()" type="button" class="btn-close btn-light close-button " aria-label="Close"></button>
        <div class="d-flex flex-column bd-highlight customer-details mb-3">
            <div class="p-2 bd-highlight" v-for="item in filterItems" :key="item.id">
                <h5 class="cus-name">{{ item.customerName }}</h5>
                <h6>Customer Number: <strong>{{ item.customerContact }}</strong> </h6>
                <h6> Current Use: <strong>{{ item.count.length + 1 }}</strong> </h6>
                <h6> First Rider: <strong> {{ item.Rider.riderName }} </strong></h6>
                <h6>Discount: <strong> N{{ item.discountAmount }} </strong> </h6>
            </div>

            <div class="p-2 bd-highlight">
                <div class="d-flex flex-row bd-highlight justify-content-between">
                    <div class=" bd-highlight"> 
                        <button class="action-button btn text-white" type="button" @click="sendEditModal()">
                            <router-link :to="{ name: 'EditRecord', params: { id: GetId }}"> 
                                <i class="far fa-edit "></i> Edit 
                            </router-link>
                        </button>
                    </div>                    
                    <div class=" bd-highlight">
                        <button class="action-button btn text-white" type="button" @click="smsPageEvent()">
                            <router-link :to="{ name: 'SingleSms', params: { id: GetId }}">
                                <i class="fas fa-envelope"></i> SMS
                            </router-link>
                            
                        </button>
                    </div>
                    <div class=" bd-highlight">
                        <button class="btn action-button text-white" type="button" @click="showDeletePage()">
                            <router-link :to="{ name: 'DeleteCustomer', params: { id: GetId }}">
                                <i class="fas fa-envelope"></i> Delete
                            </router-link>                           
                        </button>                          
                    </div>
                </div>                    
            </div>

            <div class="submitError" v-if="ErrorMessage">
                <h6 class="text-danger">an Error occured</h6>                            
            </div> 

            <div class="p-2 bd-highlight">                
                <div class="lastUsed" v-for="i in filterItems" :key="i.id">
                    <p class="mt-2 fw-bold  text-white" v-if="i.count == '' ">
                        Last Used: {{ dateRange(i.dateCreated) }}
                    </p>
                    <p class="mt-2 fw-bold text-white" v-else v-for="items in i.count.slice(0,1)" :key="items.id"> 
                        Last Used: {{ dateRange(items.dateCreated) }}
                    </p>
                </div>
            </div>

            <div class="p-2 bd-highlight">
               <div class="details-section">
                    <table class="table text-light table-borderless">
                        <thead v-for="i in filterItems" :key="i.id">
                            <tr v-if="i.count == '' "> </tr>
                            <tr v-else>
                                <th scope="col">s/n</th>
                                <th scope="col">Date</th>
                                <th scope="col">Rider</th>                                                                                      
                            </tr>
                        </thead>
                        <tbody v-for="i in filterItems" :key="i.id">
                            <div v-if="i.count == '' ">
                                <p class="nothing">Nothing to see here</p>
                            </div>
                            <tr v-else v-for="(items, index) in i.count" :key="items.id" class="text-light">                                
                                <td scope="row">{{ index + 2}}</td>
                                <td> <small> {{ dateTime(items.dateCreated) }} </small> </td>                                                            
                                <td> <small> {{ items.Rider.riderName}} </small> </td>                                                            
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
        dateTime: Function,
        dateRange: Function,
    },
    emits: ['closeDetails', 'showEditModal', 'showSection', 'showSms', 'showDelete'],

    setup(props, context) {
        const route = useRoute() 
        const GetId = computed(() => route.params.id)       
        
        const getCustomerDetails = toRef(props, 'uniqueCustomers')        
        const sendCloseEvent = () => {
            context.emit('closeDetails')
        }

        const sendEditModal = ()=> {
            context.emit('showEditModal')                        
            context.emit('showSection')
        }

        const smsPageEvent = () => {
            context.emit('showSms')
            context.emit('showSection')
        }

        const showDeletePage = () => {
            context.emit('showDelete')
            context.emit('showSection')
        }
        
        
        watch(
            () => route.params, 
            () => { filterItems }
        )
        const filterItems = computed (() => getCustomerDetails.value.filter(
                getCustomers => getCustomers.id == route.params.id
            ))        
        
        return{            
            filterItems,
            sendCloseEvent,
            GetId,
            sendEditModal,           
            smsPageEvent,                                               
            showDeletePage
        }
    },
}
</script>

<style scoped>

aside{
    background-color: #ffffff;
    height: auto;
    border-radius: 10px;
    padding: 20px;
}

.lastUsed{
    background: #2b4d83;
    border-radius: 10px;
    padding: 1px;
    box-shadow: 0px 4px 4px 0px #00000026;
    text-align: center;    
    margin-bottom: 20px;
}

.details-section{
    background-color: #40649e;
    border-radius: 10px;
    padding: 20px;
    height: 20rem;
    overflow: scroll;        
}

a {
    text-decoration: none;
    color:  #40649e;
}

a:hover{
    color: white;
}

.close-button{
    position: absolute;
    left: 17.7rem;            
}

.cus-name{
    font-family: 'Comfortaa', cursive;
    font-weight: bolder;
}

.nothing{
    font-weight: 900;
    font-size: 40px;
}

.customer-details{
    color: #40649e;
}

.action-button:hover {
    background: #2b4d83;
    border-radius: 10px;
    color: white;
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