 <template>
    <div>
        <div class="row">
            <div class="col-md-8">
                <div class="theBack">        
                <section class="sticky-top shadow-sm the-section" v-if="HideSection">
                        <div class="d-flex flex-row bd-highlight text-white justify-content-between">
                            <div class="p-2 bd-highlight ">                                               
                                <p class="lh-1">
                                    Customer Records 
                                    <br>
                                    <span><small>(Unique names)</small></span>    
                                </p>                         
                            </div>

                            <div class="p-2 bd-highlight">   
                                <p class="lh-1">
                                    <strong> Unique:</strong> <br> {{ searchedCustomers.length }}
                                </p>                                                                         
                            </div>

                            <div class="p-2 bd-highlight">                                               
                                <p class="lh-1" >
                                    <strong>Total:</strong> <br> {{ allEntries }}
                                </p>    
                            </div>

                            <div class="p-2 bd-highlight w-10">                       
                                <div class="input-group">
                                    <span class="input-group-text icon" id="basic-addon1"><i class="fas fa-search text-white"></i></span>                     
                                    <input type="text" v-model="searchName" class="form-control" placeholder="Search..." aria-describedby="basic-addon1"/>
                                    <span class="clear" @click="clearSearch()"><i class="fas fa-times"></i></span>
                                </div>                                              
                            </div>
                        </div>               

                </section>
                    <table class="table table-sm mt-3">
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
                            <tr v-for="(i, index) in searchedCustomers" :key="i.id">
                                <td>{{ index + 1 }}</td>
                                <td @click= "changeStateOnce">
                                    <router-link :to ="{name: 'RecordDetails',
                                        params: {
                                            id:i.id,
                                            customerName: i.customerName,
                                            customerContact: i.customerContact,
                                            lastUse: i.count.length + 1,
                                            firstRider: i.Rider.riderName,
                                            riderId: i.Rider.id,
                                            discount: i.discountAmount,   
                                            dateCreated: i.dateCreated                                  
                                        }                                
                                    }"
                                    >
                                        {{ i.customerName }}
                                    </router-link>
                                </td>                        
                                <td>{{ i.customerContact }}
                                    {{ i.__typename }}
                                </td>
                                <td> {{dateTime( i.dateCreated ) }} </td>
                                <td>{{ i.count.length + 1 }} </td>
                                <td v-if="i.count == '' "> 
                                    {{ dateRange(i.dateCreated) }}                                          
                                </td>     
                                <td v-else>
                                    <div  v-for="items in i.count.slice(0, 1)" :key="items.id">
                                        {{ dateRange(items.dateCreated) }}
                                    </div>  
                                </td>                                                               
                            </tr>            
                        </tbody>
                    </table>             
                </div>
            </div>
            <div class="col-md-4">
                <div class="sticky-top the-details" v-if="hidePage"                                                     >
                    <RecordDetails
                        :uniqueCustomers= "uniqueCustomers"
                        :dateTime = "dateTime"       
                        :dateRange = "dateRange"
                        @closeDetails = 'changeState'
                        @showEditModal = 'showEditModal'
                        @showSection = 'showSectionOnce'
                        @showSms = 'showSms'
                        @showDelete = 'showDelete'
                    />                                 
                </div>

            </div>    
        </div>  
        <div class="back-drop" v-if="hideEditModal">
            <EditRecords 
                :uniqueCustomers = 'uniqueCustomers'
                @showEditModal ='showEditModal'                
                @showSection ='showSection'
            />
        </div>

        <div class="back-drop" v-if="hideSms">
            <SingleSms
                @showEditModal = 'showSms'
                :uniqueCustomers = 'uniqueCustomers'
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
import  RecordDetails from '../Records/RecordsDetails.vue'
import  EditRecords from '../Records/EditRecords.vue'
import DeleteCustomer from '../DeleteCustomer.vue'
import SingleSms from '../SingleSms.vue'
import { computed, ref, toRef } from '@vue/reactivity'

export default {
    name: "recordList",

    components: {
        RecordDetails,
        EditRecords,
        SingleSms,
        DeleteCustomer
    },

    props: {
        uniqueCustomers: Object,
        multipleCustomers: Object
    },
 
    setup(props) {        
        const allCustomers = toRef(props, 'uniqueCustomers')        
        const multipleEntries = toRef(props, 'multipleCustomers')

        const searchName = ref('')
        const hidePage = ref(false)
        const changeState = () => hidePage.value = !hidePage.value
        const changeStateOnce = () => hidePage.value = true

        const hideEditModal = ref(false)
        const showEditModal = ()=> hideEditModal.value = !hideEditModal.value

        const HideSection = ref(true)
        const showSection = () => HideSection.value = !HideSection.value
        
        const showSectionOnce = () => HideSection.value = false

        const hideDelete = ref(false)
        const showDelete = () => hideDelete.value = !hideDelete.value

        const hideSms = ref(false)
        const showSms= () => hideSms.value = !hideSms.value

        const allEntries = computed(() => allCustomers.value.length + multipleEntries.value.length)                
        const searchedCustomers = computed(() => {
            return allCustomers.value.filter((allCustomer) => {
                return (
                    allCustomer.customerName
                    .toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1 ||
                    allCustomer.customerContact
                    .toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1
                )
            })
        })
        const clearSearch = () => {
            searchName.value = ''
        }

        function dateTime(value) {
            return moment(value).format('DD-MM-YYYY')
        }

        function dateRange(value) {
            return moment(value).fromNow()
        }                
        
        return{
            dateTime,
            dateRange,
            RecordDetails,
            EditRecords,
            SingleSms,
            DeleteCustomer,
            searchName,
            searchedCustomers,  
            hidePage,          
            changeState,
            changeStateOnce,
            allEntries,
            clearSearch,
            hideEditModal,
            showEditModal,
            showSection,
            HideSection,
            hideSms,
            showSms,
            showSectionOnce,
            showDelete,
            hideDelete
        }
    },
}
</script>

<style scoped>
.theBack {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 10px;
}

a {
    text-decoration: none;
}

 a.router-link-exact-active {    
    color: rgb(37, 73, 190);
    
    font-weight: bold;       
    text-align: center;
}

.the-section{
    background-color: #517fbb;
    border-radius: 20px;
    padding: 10px;
    height: 4.6rem;
}

.icon{
    background-color: #6e9fdf;
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
}

.the-details{
    z-index: 2;
    height: 400px;
}

</style>