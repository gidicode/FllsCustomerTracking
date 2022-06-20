<template>
    <aside class="shadow-sm">        

        <button @click="closeDetailsPage()" type="button" class="btn-close btn-light close-button " aria-label="Close"></button>

        <div class="d-flex flex-column bd-highlight customer-details mb-3">

            <div class="p-2 bd-highlight" v-for="item of filterCustomers" :key="item.node.id">
                <h5 class="cus-name">{{ item.node.customerName }}</h5>
                <h6>Customer Number: <strong>{{ item.node.customerContact }}</strong> </h6>
                <h6> Current Use: <strong>{{ item.node.count.length + 1 }}</strong> </h6>
                <h6> First Rider: <strong> {{ item.node.Rider.riderName }} </strong></h6>
                <h6>Discount: <strong> N{{ item.node.discountAmount }} </strong> </h6>
            </div> 

            <div class="p-2 bd-highlight">

                <div class="d-flex flex-row bd-highlight justify-content-between">
                    <div class=" bd-highlight">                         
                        <button v-if="candEditState" class="action-button btn text-white" type="button" @click="openEditRecordModal(), pushId(GetId), changeCanEdit()">                           
                                <i class="far fa-edit "></i> Edit                           
                        </button>

                        <button v-else disabled class="action-button btn text-white" type="button">                           
                                <i class="far fa-edit "></i> Editing...                     
                        </button>
                    </div>                    

                    <div class=" bd-highlight">                        
                        <button class="action-button btn text-white" type="button" @click="showPersonalSms()">                                                        
                                <i class="fas fa-envelope"></i> SMS                            
                        </button>                        
                    </div>

                    <div class=" bd-highlight">                        
                        <button class="btn action-button text-white" type="button" @click="showDeletePage()">                            
                                <i class="fas fa-envelope"></i> Delete                            
                        </button>
                    </div>
                </div>                    
            </div>

            <div class="submitError" v-if="ErrorMessage">
                <h6 class="text-danger">an Error occured</h6>                            
            </div> 

            <div class="p-2 bd-highlight">                
                <div class="lastUsed" v-for="i in filterCustomers.slice(0,1)" :key="i.id">
                    <p class="mt-2 fw-bold  text-white" v-if="i.node.count == '' ">
                        Last Used: {{ dateRange(i.node.dateCreated) }}
                    </p>
                    
                    <p class="mt-2 fw-bold text-white" v-else v-for="items in i.node.count.slice(0,1)" :key="items.id"> 
                        Last Used: {{ dateRange(items.dateCreated) }}
                    </p>
                </div>
            </div>

            <div class="p-2 bd-highlight">
               <div class="details-section">
                    <table class="table text-light table-borderless">                        
                        <thead v-for="i in filterCustomers" :key="i.id">
                            <tr v-if="i.node.count == '' "> </tr>
                            <tr v-else>
                                <th scope="col">s/n</th>
                                <th scope="col">Date</th>
                                <th scope="col">Rider</th>                                                                                      
                            </tr>
                        </thead>
                        <tbody v-for="i in filterCustomers" :key="i.id">
                            <div v-if="i.node.count == '' ">
                                <p class="nothing">Nothing to see here</p>
                            </div>
                            <tr v-else v-for="(items, index) in i.node.count" :key="items.id" class="text-light">                                
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
import { computed, toRef, watch } from 'vue'
import { useStore } from 'vuex'

export default {
    name: "RecordDetails",    
    props: {
        uniqueCustomers: Object,
        dateTime: Function,
        dateRange: Function,
        checkCustomerId: String
    },    

    setup(props) {                
        const store = useStore()
        const GetId = computed(() => store.state.customerId)
        const candEditState = computed(() => store.state.canEdit)        
        
        const getCustomerDetails = toRef(props, 'uniqueCustomers')                        

        const closeDetailsPage = () => {
            store.commit('closeRecordDetails')
        }

        const openEditRecordModal = () => {
            store.commit('openEditRecord')
        }

        const pushId = (id) => {
            store.commit('getId', id)            
        }

        const changeCanEdit = () => {
            store.commit('canEditCustomer')
        }

        const showPersonalSms = () => {
            store.commit('showPersonalSms')
            store.commit('hideRecordHeading')
        }

        const showDeletePage = () => {
            store.commit('showDeletePage')
        }
        
        watch( GetId, 
            () => { filterCustomers }
        )
        const filterCustomers = computed (() => getCustomerDetails.value.entries.edges.filter(
                getCustomers => getCustomers.node.id == GetId.value
            ))                    
        
        return{            
            filterCustomers,           
            GetId,                      
            closeDetailsPage,
            openEditRecordModal,
            pushId,            
            changeCanEdit,
            candEditState,
            showPersonalSms,
            showDeletePage,
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
    width: 350px;
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

.action-button {
    background: #3160ac;
    border-radius: 10px;
    color: white;
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