 <template>
    <div class="row">
    <div class="col-md-8">
        <div class="theBack">        
           <section class="sticky-top shadow-sm">
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
                        </div>                                              
                    </div>
                </div>               

           </section>
            <table class="table mt-3">
                <thead>
                    <tr>    
                        <th scope="col">S/N</th>        
                        <th scope="col">Customer Name</th>
                        <th scope="col">Phone Number</th>
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
                                    lastUse: i.count.length + 1 ,
                                    firstRider: i.Rider.riderName,
                                    discount: i.discountAmount,                                     
                                }                                
                            }"
                            >
                                {{ i.customerName }}
                            </router-link>
                        </td>                        
                        <td>{{ i.customerContact }}</td>
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
        <div class="sticky-top" v-if="hidePage"                                                     >
             <RecordDetails
            :uniqueCustomers= "uniqueCustomers"
            :dateTime = "dateTime"
            :dateRange = "dateRange"
            @closeDetails = 'changeState'
             />
        </div>
    </div>
    </div>
   
</template>

<script>
import moment from 'moment'
import  RecordDetails from '../Records/RecordsDetails.vue'
import { computed, ref, toRef } from '@vue/reactivity'

export default {
    name: "recordList",

    components: {
        RecordDetails,
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

        const allEntries = computed(() => allCustomers.value.length + multipleEntries.value.length)

        console.log(allEntries.value)
        
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
            searchName,
            searchedCustomers,  
            hidePage,          
            changeState,
            changeStateOnce,
            allEntries
        }
    },
}
</script>

<style scoped>
.theBack {
    background-color: #F8FBFF;
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

section{
    background-color: #517fbb;
    border-radius: 20px;
    padding: 10px;
    height: 4.6rem;
}

.icon{
    background-color: #6e9fdf;
}

</style>