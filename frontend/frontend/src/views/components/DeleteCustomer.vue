<template>
    <div class="delete-section">
        <div class="item-section">
            <div v-if="loading" class="loading-position">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <div v-if="deleted" class="text-center">
                <h4 class="text-success">Successfull</h4>
            </div>

            <div v-if="ErrorMessage">
                <h5 class="text-danger">opps, something wrong happened</h5>
            </div>
            <h6 class="ques-text" v-if="hideText"> Are you sure you want to delete this customer record? </h6>
            <p class="details" v-if="hideText">{{ CustomerDetails.node.customerName }}, {{ CustomerDetails.node.customerContact }},</p>

            <div class="d-grid gap-2 col-8 mx-auto">                
                <button class="btn btn-danger" type="button" v-if="hideText" @click="deleteRecord()" > Delete</button>
                <button class="btn btn-outline-primary" type="button" @click="closeDeletePage()" >Close</button>
            </div>
        </div>
    </div>
</template>

<script>

import { computed, toRef, ref, watch } from '@vue/runtime-core'
import { useStore } from 'vuex'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

export default {
    name: 'DeleteCustomer',    
    props: { uniqueCustomers : Object},

    setup(props) {    
        const store = useStore()
        const GetId = computed(() => store.state.customerId)        
        const getCustomerDetails = toRef(props, 'uniqueCustomers')
        const CustomerDetails = ref({})
        const deleted = ref(false)
        const hideText = ref(true)
        
        const closeDeletePage = () => {
            store.commit('closeDeletePage')
        }
        
        watch(GetId,
            () => { filterItems }
        )

        const filterItems = computed(() => getCustomerDetails.value.entries.edges.filter(
            getCustomers => getCustomers.node.id == GetId.value
        ))
        filterItems.value.forEach(element => {
            CustomerDetails.value = element
        });
        
        const { mutate: deleteRecord, error:ErrorMessage, onDone, loading} = useMutation(gql`
            mutation deleteRidersLog2($id:ID!){
             deleteRidersLog2( input : {
                id: $id
             }
             ){ 
                deleteLog {
                    id
                    }
                }
            }
        `, () => ({
            variables: { id: GetId.value}
        }))

        onDone(() => {
            deleted.value = true
            hideText.value = false
        })

        return {            
            CustomerDetails,
            deleteRecord,
            ErrorMessage,
            loading,
            deleted,
            hideText,
            closeDeletePage,
        }
        
    },
}
</script>

<style scoped>
 .delete-section {
     width: 50%;
     background-color: rgb(255, 255, 255);
     margin-left: 10%;
     margin-right: auto;
     height: inherit;
     padding: 20px;     
 }

 .ques-text{
     text-align: center;     
     margin-top: 10%;
 }

 .details{
     text-align: center;
     font-weight: 600;
     color: rgb(0, 86, 247);
 }

 .loading-position{
     justify-content: center;
     text-align: center;     
 }

 .item-section {
     margin-top: 20%;
 }
</style>