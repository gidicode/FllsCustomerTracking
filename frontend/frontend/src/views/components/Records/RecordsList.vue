<template>
    <div class="row">
    <div class="col-md-8">
        <div class="theBack">        
            <ul v-for="i in multipleCustomers" :key="i.id">           
                    <li>{{ i.customer.customerName}}</li>           
            </ul>
            <table class="table">
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
                    <tr v-for="(i, index) in uniqueCustomers" :key="i.id">                                        
                        <td>{{ index + 1 }}</td>
                        <td>
                            <router-link :to ="{name: 'RecordDetails',
                                params: {
                                    id:i.id,
                                    customerName: i.customerName,
                                    customerContact: i.customerContact,
                                    lastUse: i.count.length + 1 ,
                                    firstRider: i.Rider.riderName,
                                    discount: i.discountAmount,
                                    listDelivery: JSON.stringify(i.count)
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
        <div class="sticky-top">
             <RecordDetails/>          
        </div>
    </div>
    </div>
   
</template>

<script>
import moment from 'moment'
import  RecordDetails from '../Records/RecordsDetails.vue'

export default {
    name: "recordList",

    components: {
        RecordDetails,
    },

    props: {
        uniqueCustomers: Array,
        multipleCustomers: Array
    },
    setup() {
       
        function dateTime(value) {
            return moment(value).format('YYYY-MM-DD')
        }

        function dateRange(value) {
            return moment(value).fromNow()
        }        
        
        return{
            dateTime,
            dateRange,
            RecordDetails
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
</style>