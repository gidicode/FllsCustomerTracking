<template>
    <div class="back-drop shadow mb-3" >        

        <button @click.self="sendEditModal()" type="button" class="btn-close close-button btn-light close-button " aria-label="Close"></button>        

        <div class="form-background">
            <p class="text-primary">Edit Customer Details</p>
            <form @submit.prevent="editEntries()">
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
                    <select class="form-select" aria-label="Select Rider" id="Select-Rider" v-model= "selectRider">
                        <option selected :value="riderValueId"> {{ selectRider }} </option>                                                        
                        <option v-for="rider in getRiders" :key="rider.id" :value="rider.id">
                            {{ rider.riderName}} 
                        </option>
                    </select>
                </div>
                <span class="error-text"></span>
                
                <button class="btn btn-primary mt-4" type="button" disabled v-if="loading">
                    <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                    Loading...
                </button>  
                <button type="submit" class="btn btn-primary mt-4" v-else>Submit</button>
                
            </form>      
        
            <div class="submitError" v-if="ErrorMessage">
                <h6 class="text-danger">an Error occured</h6>                            
            </div> 
        </div>
    </div>
</template>

<script>
//import { useField, useForm } from 'vee-validate'
//import * as yup from 'yup'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useRoute } from 'vue-router'
import { computed, watch, toRef, ref} from '@vue/runtime-core'
import { GetRiders } from '../../../graphql'

export default {
    name: 'EditRecords',
    emits: ['showEditModal', 'showSection'],

    props: {
        uniqueCustomers: Object,
    },

    setup(props, context) {
        const route = useRoute()
        const customerId = computed(() => route.params.id)
        const customerNames = computed(() => route.params.customerName)
        const customerContacts = computed(() => route.params.customerContact)
        const riders = computed(() => route.params.rider)
        const riderId = computed(() => route.params.riderId)
        const Ddate = computed(() => route.params.dateCreated)
        const getCustomerDetails = toRef(props, 'uniqueCustomers')        
        
        const getRiders = computed(() => GetRiders.value)
        
        watch(
            () => route.params,
            () => { filterCustomers}
        )

        const filterCustomers = computed(() => getCustomerDetails.value.filter(
            getCustomer => getCustomer.id == customerId.value
        ))

        const customerName = ref(customerNames.value)        
        const customerContact = ref(customerContacts.value)
        const selectRider = ref(riders.value)
        const riderValueId = ref(riderId.value)
        const theDate = ref(Ddate.value)         

        const sendEditModal = ()=> {
            context.emit('showEditModal')
            context.emit('showSection')
        }               
/*
        const schema = yup.object({
            customerName: yup.string(),
            customerContact: yup.string().required().matches(/^[0-9]+$/).min(11, "Must be 11 characters").max(11, "Must be 11 characters"),
            selectRider: yup.number().positive().integer(),
            theDate: yup.date(),
        })

        useForm({
            validationSchema: schema,
        })        

        const { handleSubmit } = useForm({
            validationSchema: schema,
        })

        const onSubmit = handleSubmit(( values, { resetForm }) => {
            editEntries()            

            onDone(() => {
                resetForm({
                    values: {
                        customerName: customerName.value,
                        customerContact: customerContact.value,
                        dateCreated: theDate.value,
                        rider: selectRider.value
                    }
                })
            })
        })

        const { value: customerName, errorMessage: customerNameError } = useField('customerName')
        const { value: customerContact, errorMessage: customerContactError } = useField('customerContact')
        const { value: theDate, errorMessage: dateCreatedError } = useField('dateCreated')
        const { value: selectRider, errorMessage: selectRiderError } = useField('selectRider')
*/
        const { mutate: editEntries, onDone, 
                error: ErrorMessage, loading} = useMutation(gql`
                    mutation editRidersLog(     
                        $id: ID!,                                           
                        $customerName: String!,
                        $customerContact: String!,
                        $rider: Int!,
                        $dateCreated: DateTime!
                    ){
                        editRidersLog(  
                            id: $id,                                                      
                            customerName: $customerName,
                            customerContact: $customerContact,
                            rider: $rider,
                            dateCreated: $dateCreated
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

            onDone({
                customerName: customerName.value,
                customerContact: customerContact.value,
                rider: selectRider.value,
                dateCreated: theDate.value
            })

         return {
             sendEditModal,
             selectRider,
             theDate,
             filterCustomers,
             customerId,
             customerName,
             customerContact,
             getRiders,             
            /* customerContactError,
             customerNameError,
             dateCreatedError,
             selectRiderError,             
             onSubmit,
             */
             ErrorMessage,
             loading,
             editEntries,
             riderValueId
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
