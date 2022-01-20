<template>
    <aside>
        <div class="d-flex flex-column bd-highlight text-white mb-3">
            <div class="p-2 bd-highlight">
                <h4>{{ CustomerName }}</h4>
                <h6>Customer Number: <strong> {{ CustomerContact }}</strong> </h6>
                <h6> Current Use: <strong>{{ lastUse }}</strong> </h6>
                <h6> First Rider: <strong> {{ rider }} </strong></h6>
                <h6>Discount: <strong> N{{ discount }} </strong> </h6>
            </div>
            <div class="p-2 bd-highlight">                
                <div class="lastUsed">
                    <p class="mt-2 fw-bold">Last Used: 5 days ago</p>
                </div>
            </div>
            <div class="p-2 bd-highlight">
               <div>
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col">#</th>
                                <th scope="col">First</th>
                                <th scope="col">Last</th>
                                <th scope="col">Handle</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th scope="row">1</th>
                                <td >{{ listDeliverys }}</td>
                                <td>Otto</td>
                                <td>@mdo</td>
                            </tr>                           
                        </tbody>
                    </table>
               </div>
            </div>

            <div class="p-2 bd-highlight">
                 
                <p></p>
            </div>
        </div>      
    </aside>
</template>

<script>
import { computed } from '@vue/runtime-core'
import { useRoute } from 'vue-router'

export default {
    name: "RecordDetails",    
    props: {
        listDelivery: String
    },
    setup(props) {
        const route = useRoute() 
        const CustomerName = computed(() => route.params.customerName)
        const CustomerContact = computed(() => route.params.customerContact)
        const lastUse = computed(() => route.params.lastUse)
        const rider = computed(() => route.params.firstRider)
        const discount = computed(() => route.params.discount)
        const listDeliverys = computed(() => route.params.listDelivery)
        console.log(props.listDelivery)

        return{
            CustomerName,
            CustomerContact,
            lastUse,
            rider,
            discount,
            listDeliverys
        }
    },
}
</script>

<style scoped>
aside{
    background-color: #859BBB;
    height: auto;
    border-radius: 10px;
    padding: 10px;
}

.lastUsed{
    background: #83E38C;
    border-radius: 10px;
    padding: 1px;
    box-shadow: 0px 4px 4px 0px #00000026;
    text-align: center;    
    margin-bottom: 20px;
}
</style>