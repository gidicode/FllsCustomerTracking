<template>

    <div>
        <div class="d-flex flex-row bd-highlight rider-name mb-3 justify-content-between">
            <div class="p-2 bd-highlight">
                <h6 class="mt-2"> 
                    <span class="opacity-75"> Rider:</span> 
                    {{ RiderName }}
                </h6>                
            </div>
            <div class="p-2 bd-highlight">
                <h6 class="length-bg">
                    <span class="opacity-75"> Count: </span>
                    {{ joinedList.length }}
                </h6>
            </div>            

            <div class="p-2 bd-highlight expand">
                <div class="input-group">
                    <span class="input-group-text icon" id="basic-addon1"><i class="fas fa-search text-white"></i></span>                     
                    <input type="text" v-model="searchName" class="form-control" placeholder="Search..." aria-describedby="basic-addon1"/>
                </div>    
            </div>
        </div>        
                
        <table class="table table-hover">
            <thead>
                <tr>
                <th scope="col">S/N</th>
                <th scope="col">Date</th>
                <th scope="col">Cus. Name</th>
                <th scope="col">Cus. Number</th>                
                </tr>
            </thead>
            <tbody >
                <tr v-for="(item, index) in joinedList" :key="item.id">
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
    </div>
</template>

<script>
import { computed, ref } from '@vue/reactivity'
import { useRoute } from 'vue-router'
import { RecordQueryUnique, RecordQueryMultiple } from '../../graphql'
import { watch } from 'vue'
import moment from 'moment'

export default {
    setup() {
        const route = useRoute()
        const MultipleCustomers = computed(() => RecordQueryMultiple.value)        
        const SingleCustomer = computed(() => RecordQueryUnique.value)
        const RiderName = computed(() => route.params.name)

        function DisplayDate(value) {
            return moment(value).format('DD-MM-YYYY')
        }
         watch(
            () => route.params,
            () => {
                filterRider,
                filterRider2                
            }
        )

        const filterRider = computed(() => MultipleCustomers.value.filter(
            getRiders => getRiders.Rider.id == route.params.id
        ))        

        const filterRider2 = computed(() => SingleCustomer.value.filter(
                singleCustomers => singleCustomers.Rider.id == route.params.id
            ))

        const joinedList = computed(() => filterRider.value.concat(filterRider2.value))

        const searchName = ref('')

        const searchWater = computed(() => {
            return joinedList.value.filter((joinedListS) => {
                return (
                    console.log(joinedListS.customer),
                    joinedListS.customer
                    .toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1
                )
            })
        })
        //console.log(searchWater.value)
        return {          
            DisplayDate,
            joinedList,
            RiderName,
            searchWater,
            searchName,
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
</style>

