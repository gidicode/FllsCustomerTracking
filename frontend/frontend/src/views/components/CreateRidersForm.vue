<template>
    <div class="formDesign shadow mb-3">
        <form @submit.prevent="CreateRiders">
            <div class="mb-3">
                <label for="customerName" class="form-label">Riders Name</label>
                <input type="text" class="form-control" id="customerName" v-model= "riderName">                                
            </div>
            <div class="mb-3">
                <label for="customerContact" class="form-label"> Riders Plate Number</label> 
                <input type="text" class="form-control" id="customerContact" v-model= "riderNumber">                
            </div>            
            
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
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { ref } from '@vue/reactivity'
import { GetRiders }  from '../../graphql'



export default {
    name: 'CreateRidersForm',
    setup() {

        const riderName = ref('')
        const riderNumber = ref('')                   

        const { mutate: CreateRiders,                 
                error:ErrorMessage, 
                onDone,
                loadding } = useMutation(gql`
                    mutation  addRiders( $riderName: String!, $riderNumber: String!){
                        addRiders( riderName: $riderName, riderNumber: $riderNumber){
                            riders {
                                id
                                riderName
                                riderNumber
                            }

                        }
                    }
                `, () => ({
                    variables: {
                        riderName: riderName.value,
                        riderNumber: riderNumber.value,

                    },
                    update: (cache, { data: { addRiders } }) => {
                         const RIDERCACHE = gql`
                            query getRider {
                                ridersList {
                                    id
                                    riderName
                                }
                            }
                        `
                        
                        const data  = cache.readQuery({ query: RIDERCACHE }) 
                        console.log(addRiders)                       
                        console.log(data)
                        data.ridersList.push(addRiders)
                        cache.writeQuery({ query: RIDERCACHE, data})
                    },
                    
                }))        

                onDone(() => {
                    riderName.value = ''
                    riderNumber.value = ''
                    })

            return {
                GetRiders,
                CreateRiders,                
                ErrorMessage,
                loadding,
                riderName,
                riderNumber,
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
</style>
