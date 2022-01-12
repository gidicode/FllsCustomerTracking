<template>
   <div>        
       <ul v-for="i in multipleCustomers" :key="i.id">           
            <li>{{ i.customer.customerName}}</li>           
        </ul>
        <table class="table">
                <thead>
                    <tr>            
                        <th scope="col">Customer Name</th>
                        <th scope="col">Phone Number</th>
                        <th scope="col">Onboard</th>
                        <th scope="col">Count</th>
                        <th scope="col">Last Used</th>
                        </tr>
                </thead>
                <tbody>
                    <tr v-for="i in uniqueCustomers" :key="i.id">                
                        <td>{{ i.customerName }}</td>
                        <td>{{ i.customerContact }}</td>
                        <td>{{dateTime( i.dateCreated ) }} </td>                        
                        <td>{{ i.count.length + 1 }} </td>
                        <td v-for="items in i.count.slice(0, 1)" :key="items.id"> 
                            {{dateTime(items.dateCreated) }} 
                        </td>                        
                        
                    </tr>            
                </tbody>
            </table>
   </div>
</template>

<script>
import moment from 'moment'
//import { computed } from '@vue/reactivity'

export default {
    name: "recordList",
     props: {
        uniqueCustomers: Array,
       multipleCustomers: Array
    },
    setup() {
       
        function dateTime(value) {
            return moment(value).format('YYYY-MM-DD')
        }
        

        return{
            dateTime
        }
    },
}
</script>

