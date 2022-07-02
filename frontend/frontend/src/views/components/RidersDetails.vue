<template>

    <div class="the-body">                          
        <div v-if="load">
            <p>Loading...</p>
        </div>
        <aside v-else>                              
            <div v-if="showRidersDetails" 
                class="d-flex flex-row bd-highlight rider-name mb-3 justify-content-between sticky-top">
                <div class="p-2 bd-highlight">
                    <h6 class="mt-2"> 
                        <span class="opacity-75"> Rider:</span> 
                        {{ RiderName[0]}}
                    </h6>                
                </div>
                <div class="p-2 bd-highlight">
                    <h6 class="length-bg">
                        <span class="opacity-75"> Count: </span>
                        {{ searchRider.length }}
                    </h6>
                </div>            

                <div class="p-2 bd-highlight expand">                    
                    <div class="input-group">
                        <span class="input-group-text icon" id="basic-addon1"><i class="fas fa-search text-white"></i></span>                     
                        <input type="text" v-model="searchName" class="form-control" placeholder="Search..." aria-describedby="basic-addon1"/>
                    </div>    
                </div>
            </div>        
                
            <table class="table table-hover" v-if="showRidersDetails">
                <thead>
                    <tr>
                    <th scope="col">S/N</th>
                    <th scope="col">Date</th>
                    <th scope="col">Cus. Name</th>
                    <th scope="col">Cus. Number</th>                
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in searchRider" :key="item.id">
                        <td scope="row">{{ index + 1}}</td>
                        <td>{{ DisplayDate(item.dateCreated)}}</td> 
                        <td  v-if="item.__typename == 'MultipleEntriesType' ">
                            {{ item.customer.customerName}}
                        </td>
                        <td v-else>
                            {{item.customerName}}
                        </td>
                        <td  v-if="item.__typename == 'MultipleEntriesType' ">
                            {{ item.customer.customerContact}}
                        </td>
                        <td v-else>
                            {{ item.customerContact}}
                        </td>                                                                               
                    </tr>
                </tbody>
            </table>  

            <section v-else>
                <h1>Click on a rider name to view details</h1>
            </section>    
        </aside>   

                        
    </div>
</template>

<script>
import { computed, onMounted, ref, watch, toRef } from 'vue'
import { useStore } from 'vuex'
import { RecordQueryUnique, RecordQueryMultiple, load } from '../../graphql'
//import { watch } from 'vue'
import moment from 'moment'

export default {
    name:'RidersDetails',
    props: {
        allRiders: Object
    },
    setup(props) {
        const store = useStore()
        const getRidersId = computed(() => store.state.ridersId)
        const showRidersDetails = computed(() => store.state.showRidersDetails)
        const MultipleCustomers = computed(() => RecordQueryMultiple.value)        
        const SingleCustomer = computed(() => RecordQueryUnique.value)
        const AllRiders = toRef(props, 'allRiders')

        const RiderName = computed(() => 
            AllRiders.value.filter(item => item.id == getRidersId.value)
            .map(item => item.riderName)
        )

        function DisplayDate(value) {
            return moment(value).format('DD-MM-YYYY')
        }         

        const mergeCustomers = ref([])
        watch(load,
        () => {
            SingleCustomer.value.forEach(element => mergeCustomers.value.push(element))
            MultipleCustomers.value.forEach(element => mergeCustomers.value.push(element))            
            console.log('wow')
        })

        onMounted(() => {
            SingleCustomer.value.forEach(element => mergeCustomers.value.push(element))
            MultipleCustomers.value.forEach(element => mergeCustomers.value.push(element ))      
        })                      
    
        const filterRider = computed(() => mergeCustomers.value.filter(
            getRiders => getRiders.Rider.id == getRidersId.value
        ))                 

        const searchName = ref('')

        const searchRider = computed(() => {
            return filterRider.value.filter((item) => {
                return (                    
                    item.customerContact.toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1
                )
            })
        })

        //console.log(searchWater.value)
        return {          
            DisplayDate,            
            //RiderName,
            searchRider,
            searchName,
            getRidersId,
            filterRider,
            load,
            showRidersDetails,
            SingleCustomer,     
            mergeCustomers,
            RiderName    
        }
    },
}
</script>

<style scoped>
a{
    text-decoration: none;
    color: black;
}

.rider-name{
    background-color: #517fbb;
    padding: 10px;
    border-radius: 10px;
    color: white;
}

.length-bg{
    padding: 10px;
    background: #39649c;
}

.expand{
    width: 10rem;
}

.icon{
    background-color: #39649c;
}

.the-body{
    height: 100vh;
    overflow: scroll;
}
</style>

