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

            <div class="d-grid gap-2 col-8 mx-auto">                
                <button class="btn btn-danger" type="button" v-if="hideText" @click="DeleteMultiple" > Delete</button>
                <button class="btn btn-outline-primary mb-4" type="button" @click="closeDeleteMultiple" >Close</button>
            </div>
        </div>
    </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { ENTRIES_QUERY } from '../../graphql'

export default {
    name: 'DeleteMultiple',
    setup() {
        const store = useStore()
        const closeDeleteMultiple = computed(() => store.commit('closeDeleteMultiple'))
        const hideText = ref(true)
        const deleted = ref(false)
        const customerId = computed(() => store.state.multipleId)

        const {mutate: DeleteMultiple, 
            loading, 
            error:ErrorMessage, 
            onDone } = useMutation(gql`
                mutation deleteMultiple($id: ID!) {
                    deleteMultiple (id: $id) {
                        deleteMultiple{
                            id
                        }
                    }
                }
            `, () => ({
                variables: {id: customerId.value},
                refetchQueries: [
                     {query: ENTRIES_QUERY}
                ]
            })
            )

            onDone(() => {
                hideText.value = false
                deleted.value = true
            })

        return{
            closeDeleteMultiple,
            hideText,
            customerId,
            loading,
            ErrorMessage,
            deleted,
            DeleteMultiple

        }
    },
}
</script>

<style scoped>
 .delete-section {
     width: 50%;
     background-color: rgb(255, 255, 255);
     margin-left: auto;
     margin-right: auto;
     height: auto;
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