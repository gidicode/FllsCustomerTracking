<template>
    <section class="bg-light shadow-lg p-4 del-side">
        <h5 class="text-danger"> Selected items to delete 
            <span class="bg-secondary p-2 rounded text-white">
                {{ deleteList.length}}
            </span>
        </h5>      
        
        <div v-for="(item, index) in customersId" :key="item.id">
            <p class="text-secondary"> 
                <span class ="fw-bold">{{ index + 1 }}) </span>  
               <span class="text-dark capitalize"> {{ item.name }}: </span> {{ item.id}}
            </p>                                                         
        </div>
                     
        <div v-if="loading">
            <button 
                class="btn w-100 btn-danger d-btn" 
                @click="bulkDeleteRecord"             
                disabled
                > 
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>  
            </button>               
        </div>       
        <div v-else>
            <button 
                class="btn w-100 btn-danger d-btn" 
                @click="bulkDeleteRecord"             
                v-if="deleteList.length"> 
                    Delete all
            </button>
        </div>

        <div v-if="finishedDeleting" class="bg-success  shadow-sm d-success">
            <p  class="text-white">Deleted Successfully</p>
        </div>

        <div v-if="errorMessage" class="bg-danger shadow-sm d-success">
            <p  class="text-white">Error Occured!</p>
        </div>
        
    </section>
</template>

<script>
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { toRef, computed, ref } from 'vue'
import { ENTRIES_QUERY } from '../../graphql'

export default {

    name: "BulkDelete",
    props: {
        deleteList : Array,
    }, 

    emits: ['after-delete'],

    setup(props, ctx) {        

        const customersId = toRef(props, 'deleteList')        
        const filterList =computed(() => customersId.value.map(item => item.id))                                   
        const finishedDeleting = ref(false)
        const closeFinishEditing = () => finishedDeleting.value = false

        //const clearList = () => ctx.emit('after-delete')        

        const { mutate: bulkDeleteRecord, 
                error: errorMessage, 
                onDone,
                loading} = useMutation(gql`
                    mutation bulkDeleteLog($id:[ID!]!) {
                        bulkDeleteLog( input: {
                            id: $id
                        }
                        ){
                            bulkDeleteLog{
                                id
                            }
                        }
                    }
                `,() => ({
                    variables: { 
                        id: filterList.value
                    },

                    refetchQueries: [
                        { query: ENTRIES_QUERY}
                    ]
                }))

                onDone(() => {
                    finishedDeleting.value = true                                    
                    ctx.emit('after-delete')
                    setTimeout(closeFinishEditing, 3000)
                })

        return {
            loading,
            errorMessage,
            bulkDeleteRecord,            
            customersId,
            filterList,            
            finishedDeleting,            
        }
    },
}
</script>

<style scoped>
    .del-side{
        height: 90vh;
        overflow: scroll;
    }

    .d-btn{        
        position: relative;
        bottom: 0;
    }

    .d-rotate{
        margin-top: 50px;
        margin-left: 0;
        margin-right: 0;
    }

    .d-success{
        position: absolute;
        top: 2%;        
        right: 2%;
        
        width: fit-content;
        height: fit-content;
        padding: 10px;                             
    }

    ::-webkit-scrollbar{
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        border-radius: 50px;
    }

    ::-webkit-scrollbar-thumb {
        background-color: rgb(161, 161, 161);
        border-radius: 5px;
    }

     ::-webkit-scrollbar-thumb:hover {
        background-color: rgb(68, 68, 68);
    }

</style>