 <template>
    <div class="container-fluid">        
        <div class="row">
            <div class="col-md-8">
                <div class="theBack">        
                    <div class="sticky-top d-heading" 
                        v-if="recordsHeadingState">
                        <RecordsHeading 
                        :allEntries = 'allEntries'
                        :allCustomers = 'allCustomers'
                        />                                            
                    
                        <p 
                            class="text-primary mt-2" 
                            @click="bulkDeleteStateShow"
                            v-if="!bulkDelete">
                                Delete
                        </p> 
                        
                        <button 
                            class="btn btn-sm btn-outline-primary mt-2 " 
                            @click="bulkDeleteStateHide" 
                            v-if="bulkDelete"> 
                                Abort Delete
                        </button>                        
                    </div>                                                                                                            

                    <div v-if="loading">
                        loading...
                    </div>                                        
                  
                    <table class="table table-sm" v-else-if="result && result.entries.edges">                        

                        <thead>
                            <tr>    
                                <th scope="col" v-if="bulkDelete">Select</th>  
                                <th scope="col">S/N</th>        
                                <th scope="col">Name</th>
                                <th scope="col">Number</th>
                                <th scope="col">Onboard</th>
                                <th scope="col">Count</th>
                                <th scope="col">Last Used</th>                        
                            </tr>
                        </thead>                                                                
                                   
                        <tbody>                                                        
                            <tr @click="customersId(i.node.id)" 
                                class="t-hover" v-for="(i, index) of allCustomers" :key="i.node.id">
                                <td v-if="bulkDelete">                                                               
                                    <div class="form-check">
                                        <input                                             
                                            class="form-check-input" 
                                            type="checkbox" 
                                            v-model="check"
                                            :value="{name:i.node.customerName, id: i.node.id }"                                            
                                            :id="i.node.id"
                                             >                                        
                                    </div>
                                </td>
                                <td>{{ index + 1 }}</td>
                                <td @click="openRecordDetails()">                                                           
                                     {{ i.node.customerName}}                                     
                                </td>
                                <td>{{ i.node.customerContact}} </td>
                                <td> {{dateTime( i.node.dateCreated ) }} </td>
                                <td> {{ i.node.count.length + 1}}</td>
                                <td v-if="i.node.count == '' "> 
                                    {{ dateRange(i.node.dateCreated) }}                                          
                                </td>     
                                <td v-else>
                                   <span v-for="items in i.node.count.slice(0, 1)" :key="items.id">
                                       {{ dateRange(items.dateCreated) }}
                                    </span>
                                </td>
                            </tr>                                                                                                                                                        
                        </tbody>                        
                    </table>             
                </div>
            </div>
            <div class="col-md-4">                 
                <aside class="sticky-top" v-if="bulkDelete">
                    <BulkDelete
                    :deleteList ='check'
                    @after-delete='clearCheck'
                    />
                </aside>

                <aside class="sticky-top the-details" v-if="detailsState">                    
                    <RecordDetails
                        :uniqueCustomers= "result"
                        :dateTime = "dateTime"       
                        :dateRange = "dateRange"                        
                    />                                                     
                </aside>

                <aside class="back-drop" v-if="editRecordState">
                    <EditRecords 
                    :uniqueCustomers = 'result'/>
                </aside>

                <aside class="back-drop" v-if="smsState">
                    <SingleSms
                    :uniqueCustomers = 'result'/>
                </aside>

                <aside class="back-drop" v-if="deletePageState">
                    <DeleteCustomer
                    :uniqueCustomers = 'result'/>
                </aside>

                <aside class="back-drop" v-if="editMutiple">
                    <editMultipleRecord 
                    :multipleCustomers = 'result'/>
                </aside>

                <aside class="back-drop" v-if="deleteMutipleState">
                    <DeleteMultiple 
                    :multipleCustomers = 'result'/>
                </aside>
            </div>    
        </div>                                  
    </div>
</template>

<script>
import moment from 'moment'
import { useStore } from 'vuex'
import RecordDetails from '../Records/RecordsDetails.vue'
import EditRecords from '../Records/EditRecords.vue'
import DeleteCustomer from '../DeleteCustomer.vue'
import SingleSms from '../SingleSms.vue'
import BulkDelete from '../BulkDelete.vue'
import DeleteMultiple from '../DeleteMultiple.vue'
import editMultipleRecord from '../Records/editMultipleRecord.vue'
import { ENTRIES_QUERY } from '../../../graphql'
import { useQuery } from '@vue/apollo-composable'
import { computed, ref } from 'vue'
import RecordsHeading from '../Records/RecordsHeading.vue'
import { onUnmounted,  } from '@vue/runtime-core'

export default {
    name: "recordList",
    components: {
        RecordDetails,
        EditRecords,
        SingleSms,
        DeleteCustomer,
        RecordsHeading,
        BulkDelete,
        editMultipleRecord,
        DeleteMultiple
    },    

    props: {      
        multipleCustomers: Object,
    },
 
    setup() {                                                   
        /*const allCustomers = toRef(props, 'uniqueCustomers')        
        const multipleEntries = toRef(props, 'multipleCustomers')       */
        const store = useStore()

        //commit
        const openRecordDetails = () => {
            store.commit('openRecordDetails')
        }          
        
        //Send Id to store
        const customersId = (item) => {
            store.commit('getId', item)
        }                 
        
        //State
        const detailsState = computed(() => store.state.recordDetailsState)
        const editRecordState = computed(() => store.state.editRecordState)                                         
        const recordsHeadingState = computed(() => store.state.recordsHeadingState)                                         
        const smsState = computed(() => store.state.personalSms)
        const deletePageState = computed(() => store.state.deletePageState)
        const editMutiple = computed(() => store.state.editMultipleState)
        const deleteMutipleState = computed(() => store.state.deleteMultipleState)

        onUnmounted(() => {
            store.commit('closeRecordDetails')                        
        })

        const bulkDelete = ref(false)
        const bulkDeleteStateShow = () => bulkDelete.value = true
        const bulkDeleteStateHide = () => {
                bulkDelete.value = false
                check.value = []
            }
        const check = ref([])        

        const clearCheck = () => check.value = []
        //const deleteItemsId = ([])        

        //send Deleted Customers to store
        //const sendDeleteList = (items) => {
        //    store.commit('deleteItemsList', items)
        //}

        //const allEntries = computed(() => allCustomers.value.length + multipleEntries.value.length)                                

        function dateTime(value) {
            return moment(value).format('DD-MM-YYYY')
        }

        function dateRange(value) {
            return moment(value).fromNow()
        }   
        
        const { result, fetchMore, loading} = useQuery(ENTRIES_QUERY)                          

        const allCustomers = computed(() => result.value?.entries.edges ?? [])    	        

         function loadMore () {                                           
            fetchMore({
                variables: {
                    cursor: result.value.entries.pageInfo.endCursor
                },
                updateQuery: (previousResult, { fetchMoreResult }) => {                    
                    const newEdges = fetchMoreResult.entries.edges
                    const pageInfo = fetchMoreResult.entries.pageInfo                                                                                
                  
                    return newEdges.length ? {                                            
                        ...previousResult,                        
                        entries: { 
                            ...previousResult.entries,
                            //concat edges
                        edges: [                                                                
                                ...previousResult.entries.edges,
                                //filterOut Duplicate results from cache
                                ...newEdges.filter(n => ! previousResult.entries.edges.some(p => p.node.id === n.node.id))                                
                            ],

                            //overide with new pageInfo
                            pageInfo,
                        }
                    } : previousResult
                },
            })
            }

        window.addEventListener("scroll",  () => {
            const { scrollTop, scrollHeight, clientHeight } = document.documentElement            
            if (scrollTop + clientHeight >= scrollHeight - 5 
                && result.value.entries.pageInfo.hasNextPage) {
                loadMore()                
            }            
        }, {
            passive: true
        })
        
        return {
            dateTime,
            dateRange,
            RecordDetails,
            EditRecords,
            SingleSms,
            RecordsHeading,
            DeleteCustomer,   
            editMultipleRecord,

            openRecordDetails,          
            //state
            detailsState,
            editRecordState,
            recordsHeadingState,
            smsState,
            deletePageState,
            deleteMutipleState,

            customersId,            

            allCustomers,
            //allEntries, 
            
            result,
            loading,            
            loadMore,

            check,
            bulkDelete,
            bulkDeleteStateShow,
            bulkDeleteStateHide,

            //emitt
            clearCheck,

            editMutiple

        }
    },
}
</script>

<style scoped>
.theBack {
    background-color: #ffffff;
    padding: 30px;                         
    min-height: 50%;
}

.clear {
    position: relative;
    right: 20px;
    color: darkblue;
    margin-top: 8px;
    z-index: 4;    
}

.back-drop{      
    padding: 28px;    
    top: 0px;
    position: fixed;
    width: 100%;
    height: 100%;
    right: 0px;
    left: 0px;
    bottom: 0px;
    background: rgba(0, 0, 0, 0.5);        
    z-index: 4;
}

.the-details{
    z-index: 2;
    height: 400px;
    position: fixed;
}

.t-hover:hover {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.0)
} 

.d-heading{
    z-index: 1;
}
</style>