<template>
    <div class="back-drop shadow mb-3" >        

        <button @click.self="hideEditModal()" type="button" class="btn-close close-button btn-light close-button " aria-label="Close"></button>        

        <div class="form-background">
            <p class="text-primary">Edit Customer Details</p>
            <form>
                <div class="mb-3">
                    <label for="customerName" class="form-label">Customer Name</label>
                    <input type="text" class="form-control" id="customerName" v-model= "customerName">                
                    <span class="error-text"></span>
                </div>
                <div class="mb-3">
                    <label for="customerContact" class="form-label">Customer Phone</label>
                    <input type="text" class="form-control" id="customerContact" v-model= "customerContact">
                    <span class="error-text"></span>
                </div>                

                <div>
                    <label for="Date" class="form-label"> Date</label>
                    <input id="Date" type="text" class="form-control" v-model= "theDate">
                    <span class="error-text"></span>                
                </div>
                
                <div class="mt-3">
                    <label for="Select-Rider" class="form-label"> Select Rider</label>
                    <select class="form-select" aria-label="Select Rider" id="Select-Rider" v-model = "selectRider">
                        <option selected :value="riderId"> {{ selectRider }} </option>                                                        
                        <option v-for="rider in getRiders" :key="rider.id" :value="rider.id" >
                            {{ rider.riderName}} 
                        </option>
                    </select>
                </div>                
            
                <button class="btn btn-primary mt-4" type="button" disabled v-if="loading">
                    <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                    Loading...
                </button>  
                <button type="button" class="btn btn-primary mt-4" @click="editEntries" v-else>Save</button>                
            </form>      
          
            <div class="submitError" v-if="ErrorMessage">
                <h6 class="text-danger">An error occured</h6>                                            
            </div> 

            <div class="" v-if="Done">
                <h6 class="text-success">
                    Successfull
                </h6>
            </div>

        </div>
    </div>
</template>

<script>
import { GetRiders } from '../../../graphql'
import { computed, watch, toRef, ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

export default {
    name: 'EditRecords',    

    props: {
        uniqueCustomers: Object,
    },

    setup(props) {        
        const store = useStore()
        const customerId = computed(() => store.state.customerId)
        const getCustomerDetails = toRef(props, 'uniqueCustomers')                        

        const hideEditModal = () => {
            store.commit('openEditRecord'),
            store.commit('showRecordHeading')
            store.commit('canEditCustomer')
        }

        watch( customerId,
            () => { filterCustomersToEdit}
        )

        const filterCustomersToEdit = computed (() => getCustomerDetails.value.entries.edges.filter(
            getCustomers => getCustomers.node.id == customerId.value
        ))
        const customerInstance = ref({})
        //looping to get the instance of the filtered customers and send to customerInstance
         filterCustomersToEdit.value.forEach(element => { customerInstance.value = element})        

        //Customer Instance
        const customerNames = computed(() => customerInstance.value.node.customerName)
        const customerContacts = computed(() => customerInstance.value.node.customerContact)        
        const selectRiders = computed(() => customerInstance.value.node.Rider.riderName)             
        //setting default rider Id if no option is selected
        const riderId = computed(() => customerInstance.value.node.Rider.id)
        const theDates = computed(() => customerInstance.value.node.dateCreated)

        const Done = ref(false)   

        //Data sent from customerInstance/v-model
        const customerName = ref(customerNames.value)
        const customerContact = ref(customerContacts.value)
        const selectRider = ref(selectRiders.value)
        const theDate = ref(theDates.value)

        console.log("select", riderId.value)

        //Getting list of riders to choose from
        const getRiders = computed(() => GetRiders.value)   
        const RiderId = ref(null)        

        //getting rider Id
        watch( selectRider, 
            () => { console.log("riderId", RiderId.value)}
        )
        
        onMounted(() => {
            store.commit('hideRecordHeading')
        })
        
         

         const { mutate: editEntries, onDone,
                error: ErrorMessage, loading} = useMutation(gql`
                    mutation editRidersLog2(     
                        $id: ID!,                                           
                        $customerName: String!,
                        $customerContact: String!,
                        $rider: Int!,
                        $dateCreated: DateTime!
                    ){
                        editRidersLog2( input: {
                            id: $id,                                                      
                            customerName: $customerName,
                            customerContact: $customerContact,
                            rider: $rider,
                            dateCreated: $dateCreated
                        }                              
                        ){
                            editLog {    
                                id                            
                                customerName
                                customerContact 
                                Rider {                                    
                                    id
                                    riderName
                                }
                                dateCreated
                            }
                        }
                    }
                `, () => ({
                    variables: {
                        id: customerId.value,
                        customerName: customerName.value,
                        customerContact: customerContact.value,
                        rider: selectRider.value,
                        dateCreated: new Date(theDate.value)                  
                    },
                })
            )            
            onDone(() => {
                Done.value = true
            })           

        return {
            customerId,
            customerName,
            customerContact,
            selectRider,            
            theDate,
            Done,
            hideEditModal,
            getRiders,
            ErrorMessage,
            loading,
            editEntries,            
            riderId
        }
    }   
}
</script>

<style scoped>
.error-text {
    font-size: 11px;
    color: red;
}

.form-background{
    width: 30%;
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin-right: auto;
    margin-left: auto;
    margin-top: 20px;    
}

.close-button{
    background-color: white;
}


</style>
