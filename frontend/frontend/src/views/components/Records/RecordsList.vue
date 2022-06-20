 <template>
    <div class="container-fluid">        
        <div class="row">
            <div class="col-md-8">
                <div class="theBack">        
                    <div class="sticky-top" v-if="recordsHeadingState">
                        <RecordsHeading 
                        :allEntries = 'allEntries'
                        :allCustomers = 'allCustomers'
                        />                                            
                    </div>                                                                                        
                    <div v-if="loading">
                        loading...
                    </div>
                  
                    <table class="table table-sm mt-3" v-else-if="result && result.entries.edges">
                        <thead>
                            <tr>    
                                <th scope="col">S/N</th>        
                                <th scope="col">Name</th>
                                <th scope="col">Number</th>
                                <th scope="col">Onboard</th>
                                <th scope="col">Count</th>
                                <th scope="col">Last Used</th>                        
                            </tr>
                        </thead>                                                                
                                   
                        <tbody>                                                        
                            <tr @click="openRecordDetails(),
                                customersId(i.node.id)" 
                                class="t-hover" v-for="(i, index) of result.entries.edges" :key="i.node.id">
                                <td>{{ index + 1 }}</td>
                                <td>                                                           
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
                            <div v-if="loading">
                                loading...
                            </div>                                                        
                        </tbody>                        
                    </table>             
                </div>
            </div>
            <div class="col-md-4">                               
                <div class=" the-details" v-if="detailsState">                    
                    <RecordDetails
                        :uniqueCustomers= "result"
                        :dateTime = "dateTime"       
                        :dateRange = "dateRange"                        
                    />                                                     
                </div>
            </div>    
        </div>  
        <div class="back-drop" v-if="editRecordState">
            <EditRecords 
                :uniqueCustomers = 'result'
                @showEditModal ='showEditModal'                
                @showSection ='showSection'
            />
        </div>

        <div class="back-drop" v-if="smsState">
            <SingleSms
                @showEditModal = 'showSms'
                :uniqueCustomers = 'result'
            />
        </div>

        <div class="back-drop" v-if="hideDelete">
            <DeleteCustomer
                :uniqueCustomers = 'uniqueCustomers'
                @showDelete = 'showDelete'
            />
            <h5>gello</h5>
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
import { ENTRIES_QUERY } from '../../../graphql'
import { useQuery } from '@vue/apollo-composable'
import { computed, toRef} from '@vue/reactivity'
import RecordsHeading from '../Records/RecordsHeading.vue'
import { onUnmounted } from '@vue/runtime-core'
//import { ref} from 'vue'

export default {
    name: "recordList",
    components: {
        RecordDetails,
        EditRecords,
        SingleSms,
        DeleteCustomer,
        RecordsHeading
    },

    props: {
        uniqueCustomers: Object,
        multipleCustomers: Object,        
    },
 
    setup(props) {                                                   
        const allCustomers = toRef(props, 'uniqueCustomers')        
        const multipleEntries = toRef(props, 'multipleCustomers')       
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

        onUnmounted(() => {
            store.commit('closeRecordDetails')                        
        })

        const allEntries = computed(() => allCustomers.value.length + multipleEntries.value.length)                                

        function dateTime(value) {
            return moment(value).format('DD-MM-YYYY')
        }

        function dateRange(value) {
            return moment(value).fromNow()
        }   
        
        const { result, fetchMore, loading } = useQuery(ENTRIES_QUERY, () => ({
            notifyOnNetworkStatusChange : true,
        }))                          
           
        
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

            openRecordDetails,          
            //state
            detailsState,
            editRecordState,
            recordsHeadingState,
            smsState,

            customersId,            

            allCustomers,
            allEntries, 
            
            result,
            loading,            
            loadMore

        }
    },
}
</script>

<style scoped>
.theBack {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 10px;                      
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

</style>