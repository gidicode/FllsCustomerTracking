<template>
    <div class="formDesign shadow mb-3">        
        <form @submit.prevent="onSubmit()">
            <div class="mb-3">
                <label for="customerName" class="form-label">Customer Name</label>
                <input type="text" class="form-control" id="customerName" v-model= "customerName">                
                <span class="error-text">{{ customerNameError }}</span>
            </div>
            <div class="mb-3">
                <label for="customerContact" class="form-label">Customer Phone</label>
                <input type="text" class="form-control" id="customerContact" v-model= "customerContact">
                <span class="error-text">{{ customerContactError }}</span>
            </div>
            <div class="mb-3">
                <label for="Discount" class="form-label">Discount</label>
                <input type="number" class="form-control" id="Discount" v-model= "Discount">
                <span class="error-text">{{ DiscountError }}</span>
            </div>

            <div>
                <label for="Date" class="form-label"> Date</label>
                <input id="Date" type="date" class="form-control" v-model= "dateCreated">
                <span class="error-text">{{ dateCreatedError }}</span>                
            </div>
            
            <div class="mt-3">
                <label for="Select Rider" class="form-label"> Select Rider</label>
                <select class="form-select" aria-label="Select Rider" id="Select Rider" v-model= "selectRider">
                    <option selected disabled>Open this select menu</option>
                    <option v-for="riders in Riders" :key="riders.id" :value="riders.id">
                        {{ riders.riderName }} {{ riders.riderNumber}}
                    </option>
                </select>
            </div>
            <span class="error-text">{{ selectRiderError }}</span>
            
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
</template>

<script>
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useStore } from 'vuex'
import { computed, watch } from 'vue'
import { ENTRIES_QUERY } from '../../graphql'

export default {
    name: 'EntriesForm',
    props: {
        Riders: Array
    },

    setup() {
        const store = useStore()             
        const searchNamess = computed(() => store.state.searchNameNumer)
        const schema = yup.object({
            customerName: yup.string(),
            customerContact: yup.string().required().matches(/^[0-9]+$/).min(11, "Must be 11 characters").max(11, "Must be 11 characters"),
            Discount: yup.number().integer(),
            dateCreated: yup.date(),
            selectRider: yup.number().positive().integer(),
        })

        //Initalizing the cache
        const { result } = useQuery(ENTRIES_QUERY)  
        
        useForm({ 
            validationSchema: schema,
        })

        const { handleSubmit } = useForm({
            validationSchema: schema,
        })

        const onSubmit = handleSubmit(( values, { resetForm }) => {
            createDailyEntries()
            onDone(() => {
                resetForm({
                    values: {
                        customerName: '',
                        customerContact: '',
                        Discount: '0',
                        dateCreated: dateCreated.value,
                        selectRider: selectRider.value,
                    }
                })
            })
        })

        const { value: customerName, errorMessage: customerNameError } = useField('customerName')
        const { value: customerContact, errorMessage: customerContactError} = useField('customerContact')
        const { value: dateCreated, errorMessage: dateCreatedError } = useField('dateCreated')
        const { value: Discount, errorMessage: DiscountError } = useField('Discount')
        const { value: selectRider, errorMessage: selectRiderError } = useField('selectRider')                        

        watch( 
            () => searchNamess.value,
            () => { customerContact.value = searchNamess.value}
        )        

        const { mutate: createDailyEntries, 
                onDone, 
                error: ErrorMessage,
                loading } = useMutation(gql`
                    mutation createRidersLog2(                        
                        $customerName:String!, 
                        $customerContact: String!,
                        $rider:Int!,
                        $discountAmount: String!,
                        $dateCreated: DateTime! 
                    ){
                        createRidersLog2 ( input: {
                        customerName: $customerName,
                        customerContact: $customerContact,
                        rider: $rider,
                        discountAmount: $discountAmount,
                        dateCreated: $dateCreated,
                        }
                        ){
                            ridersLog {
                                id
                                customerName
                                customerContact                                
                                discountAmount
                                dateCreated
                                Rider {
                                    id
                                    riderName
                                    riderNumber
                                }
                            }                   
                        }
                    }
                `, () => ({
                    variables: {
                        customerName: customerName.value,
                        customerContact: customerContact.value,
                        rider: selectRider.value,
                        discountAmount: Discount.value,
                        dateCreated: new Date(dateCreated.value)
                    },                                           

                    update: (cache, { data: { createRidersLog2 } }) => {                        
                        let data = cache.readQuery({ query: ENTRIES_QUERY })
                        data = {
                                ...data,
                                edges: [  
                                    ...data.entries.edges, 
                                    createRidersLog2
                                ]                         
                            }                                                
                        cache.writeQuery({ query: ENTRIES_QUERY, data })                                               
                    },          

                   refetchQueries: [
                    {query: ENTRIES_QUERY}
                   ],
                })
            )        

         return {
            customerNameError,
            customerContactError,
            DiscountError,
            selectRiderError,
            dateCreatedError,
            onSubmit,
            ErrorMessage,
            loading,
            customerName,
            customerContact,
            Discount,
            selectRider,
            dateCreated,
            searchNamess,
            result
        }  
    },   
}
</script>

<style scoped>
.formDesign {    
    background-color: #F9F9F9;
    border-radius: 20px;
    padding: 28px;
    width: 25rem;
}

.error-text {
    font-size: 11px;
    color: red;
}
</style>
