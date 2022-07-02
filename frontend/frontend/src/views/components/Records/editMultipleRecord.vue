<template>
    <div>
        
        <button @click.self="hideEditMultiple()" type="button" class="btn-close close-button btn-light close-button " aria-label="Close"></button>        
        <form class="formDesign mt-4">                                
            <div>               
                <label for="Date" class="form-label"> Date</label>
                <input id="Date" type="text" class="form-control" v-model= "dateCreatedModel">
                <span class="error-text">{{ dateCreatedError }}</span>                
            </div>

            <div class="mt-3">
                <label for="Select Rider" class="form-label"> Select Rider</label>
                <select class="form-select" aria-label="Select Rider" id="Select Rider" v-model="ridervalue">
                    <option selected disabled>{{ ridervalue}}</option>
                    <option v-for="riders in AllRiders" :key="riders.id" :value="riders.id">
                        {{ riders.riderName }} {{ riders.riderNumber}}
                    </option>
                </select>
            </div> 

            <button class="btn btn-primary mt-4" type="button" disabled v-if="loading">
                <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                Loading...
            </button>
            <button type="submit" class="btn btn-primary mt-4" @click="editMultiples" v-else>Save</button>
            <p v-if="finished" class="text-success">
                Successfull
            </p>            
        </form>
    </div>    
</template>

<script>
import { computed, toRef, ref} from 'vue'
import { useStore } from 'vuex'
import { GetRiders } from '../../../graphql'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

export default {
    name: "editMultipleRecord",
    props: {
        multipleCustomers: Object,
    },

    setup(props) {
        const store = useStore()
        const customer = toRef(props, 'multipleCustomers')
        const finished = ref(false)

        const customerId = computed(() => store.state.multipleId)
        const nodeId = computed(() => store.state.customerId)
        const hideEditMultiple = () => store.commit('closeEditMultiple')

        const customerInstance = ref(null)
        //get the customer Instance
        const filterCustomerToEdit = computed(() => customer.value.entries.edges.filter(items => 
            items.node.id == nodeId.value)            
            )
        //getting result       
        filterCustomerToEdit.value.forEach(element => customerInstance.value = element.node.count)

        //filtering customerinstance for to get id to edit
       const gettigMultipleId = computed(() => customerInstance.value.filter(items => 
            items.id == customerId.value
        ).map(item => {customerInstance.value = item}))

        gettigMultipleId.value
            
        //customerInstance
        const dateCreated = computed(() => customerInstance.value.dateCreated)
        const Rider = computed(() => customerInstance.value.Rider.riderName)       
    
        //v-model
        const dateCreatedModel = ref(dateCreated.value)
        const ridervalue = ref(Rider.value)              
                
        const AllRiders = computed(() => GetRiders.value)

        const { mutate: editMultiples, onDone, loading } = useMutation( gql`
            mutation editMultiple($id: ID!, $dateCreated: DateTime!, $rider: Int!){
            editMultiple( id: $id, dateCreated: $dateCreated, rider: $rider){
                multiple {
                    id
                    dateCreated
                    Rider{
                        id
                        riderName
                    }
                }
            }
        }
        `,
            () => ({
                variables: {
                    id: customerId.value,
                    dateCreated: dateCreatedModel.value,
                    rider: ridervalue.value
                },            
            })
        )

        onDone(() => {
            finished.value = true
        })

        return {
            customer,
            AllRiders,
            customerId,
            filterCustomerToEdit,            
            //instance
            dateCreated,
            Rider,
            //v-model
            dateCreatedModel,
            ridervalue,
            hideEditMultiple,
            customerInstance,
            finished,
            editMultiples,
            loading
        }
        
    },
}
</script>

<style scoped>
.formDesign {    
        background-color: #F9F9F9;
        border-radius: 0px;
        padding: 30px;
        width: 25vw;
}

</style>