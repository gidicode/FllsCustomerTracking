<template>
    <div>        
        <div class="row">           
            <div class="col-md-6">                                
                <div class="form-background bg-white p-4 rounded">            
                    <h6 class="text-primary mb-3">Compose and send SMS to selected customers.</h6>
                    <form @submit.prevent="SendSMS()">                               
                        <div class="mb-3">
                            <label for="customerContact" class="form-label">Customer Contacts</label>                    
                            <textarea 
                                name="smsBody" 
                                class="form-control mb-2 bg-light " 
                                id="smsBody" 
                                v-model="checkedNames" 
                                cols="30" 
                                rows="5" 
                                disabled>
                            </textarea>                            
                            <div v-if="checkedNames.length">
                                <small class="text-primary bg-light shadow-sm rounded p-2 mt-4 w-100 mr-2"> 
                                    {{checkedNames.length}} contacts selected                               
                                </small>    

                                <small class="text-primary bg-light shadow-sm rounded p-2 mt-4 mr-2">
                                    Unit: {{ checkedNames.length * 2}}
                                </small>

                                <small class="text-primary bg-light shadow-sm rounded p-2 mt-4">
                                    Amount: N{{ checkedNames.length * 2 * 2}}
                                </small>
                            </div>                                                    
                            <small class="text-secondary" v-else>No number selected</small> 
                        </div>

                        <div>
                            <label for="smsBody" class="form-label"> Message Body</label>                    
                            <textarea 
                                name="smsBody" 
                                class="form-control" 
                                id="smsBody" 
                                v-model="Message" 
                                cols="30" 
                                rows="3">
                            </textarea>
                            <span class="error-text"></span> 
                        </div>

                        <div class=" mx-auto d-grid gap-2">
                            <button class="btn btn-primary btn-span mt-4" type="button" disabled v-if="loading">
                                <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                                Sending...
                            </button>  
                            <button type="submit" class="btn btn-primary mt-4" v-else>Send</button>
                        </div>                        

                        <div class="success" v-if="success">
                            <p class="text-success">{{ resultMessage }}</p> 
                        </div>

                        <div class="error" v-if="smsError">
                            <p class="text-danger"> {{ resultMessage }}</p> 
                        </div>                            
                    </form>                  
                </div>
            </div>

            <div class="col-md-6">               
                <section class="bg-white section-height p-3 rounded-3 shadow-sm sticky-top">
                    <div class="d-flex flex-row bd-highlight text-white justify-content-start">
                        <div class="p-2 bd-highlight "> 
                            <div v-if="isCheckAll">                        
                                <button type="submit"  @click='checkall' class="btn btn-sm rounded-3">Unselect all</button>                       
                            </div>    
                            <div v-else>
                                <div class="form-check form-switch mt-2">
                                    <input 
                                        @click='checkall'
                                        v-model='isCheckAll'
                                        class="form-check-input" 
                                        type="checkbox"                                             
                                        role="switch"
                                    />
                                    <label class="form-check-label text-secondary">Select all</label>
                                </div>    
                            </div>  
                        </div>                            
                        <!--BR-->
                        <div class="p-2 bd-highlight"> 
                            <div class="input-group">                                    
                                <input type="text" v-model="searchCustomer" class="form-control rounded-3" placeholder="Search..." aria-describedby="basic-addon1"/>
                                 <span class="clear" @click="clearSearch()">
                                     <button type="button" class="btn"> <i class=" fas fa-times"></i></button>
                                </span>
                            </div> 
                        </div>
                    </div>                                   
                </section>

                <div class="p-2 table-scroll mt-4 bg-light">
                    <table class="table">
                        <thead>
                            <tr>                                                                      
                                <th scope="col">S/N</th> 
                                <th scope="col">Name</th>                                   
                                <th scope="col">Select Contact</th>  
                                <th scope="col">Action</th>  
                            </tr>
                        </thead>
                        <tbody >
                            <tr v-for="(item, index) in searchedCustomers" :key="item.id">                           
                                <td scope="row"> {{ index + 1 }} </td>
                                <td> {{ item.customerName }} </td>                                                                                    
                                <td> {{ item.customerContact}} </td>
                                <td>                                                               
                                    <div class="form-check">
                                        <input 
                                            @click="change"
                                            class="form-check-input" 
                                            type="checkbox" 
                                            :value="item.customerContact" 
                                            :id="item.id"
                                            v-model="checkedNames">                                        
                                    </div>
                                </td>
                            </tr>                        
                        </tbody>
                    </table>   
                </div>
            </div>
        </div>        
    </div>

</template>

<script>
import { computed } from '@vue/reactivity'
import { ref } from 'vue'

import { RecordQueryUnique } from '../../graphql'

export default {

    name: 'SendSms',
    setup() {

        const uniqueCustomers = computed(() => RecordQueryUnique.value )                               

        const checkedNames = ref([]) 
        const isCheckAll = ref(false)
        const Message = ref('')        
        const searchCustomer = ref('')
        const GettingResult = ref('')
        const loading = ref(false)
        const success = ref(false)
        const smsError = ref(false)
        const resultMessage = ref('')

        const changeLoadingState = () => loading.value = !loading.value
        const changeSuccessState = () => success.value = !success.value
        const changeSmsErrorState = () => smsError.value = !smsError.value        

        const checkall = (() => {            
            isCheckAll.value = !isCheckAll.value            

            if (isCheckAll.value && checkedNames.value.length == 0) {                
                uniqueCustomers.value.forEach(element => {                
                    checkedNames.value.push(element.customerContact)
                });
            } else {                
                checkedNames.value = []                            
            }            
        })

        const change = (() => {
            isCheckAll.value = false
        })

        const searchedCustomers = computed(() => {
            return uniqueCustomers.value.filter((uniqueCustomer) => {
                return(
                    uniqueCustomer.customerName
                    .toLowerCase()
                    .indexOf(searchCustomer.value.toLowerCase()) != -1 ||
                    uniqueCustomer.customerContact
                    .toLowerCase()
                    .indexOf(searchCustomer.value.toLowerCase()) != -1
                )
            })
        })

        const clearSearch = () => {
            searchCustomer.value = ''
        }

        const SendSMS = (() => {
            var raw = {
                "sender_name" : "FLLS",
                "message": '',
                "recipients": checkedNames.value,
            }

            raw.message = Message.value

            var requestOptions = {
            method: 'POST',
            body: JSON.stringify(raw),
            redirect: 'follow',
            headers: {
                'Authorization': 'Bearer E9jriOUBg5ssOLSAc6DzE94O9cjxQ5kB6iW7DEv6mEADXs5Q2QcPXgOS0AVL',
                'Content-Type' : 'application/json'                
            },

            };

            fetch("https://app.multitexter.com/v2/app/sendsms", requestOptions)
            .then(response => response.text())
            .then(result => {
                changeLoadingState()
                console.log(result)
                GettingResult.value = JSON.parse(result)                      
                if (GettingResult.value.status !== 1) {
                    smsError.value = true
                    changeLoadingState()
                    resultMessage.value = GettingResult.value.msg
                }else if (GettingResult.value.status === 1 ) {
                    changeSuccessState()
                    changeLoadingState()
                    resultMessage.value = GettingResult.value.msg
                }
            })
            .catch(error => {
                if(error){
                    changeSmsErrorState()
                    changeLoadingState()
                    resultMessage.value = GettingResult.value.msg
                }
            });        
        })
        
        return {
            uniqueCustomers,                              
            checkedNames,
            isCheckAll,            
            checkall,
            Message,
            SendSMS,
            change,
            searchedCustomers,
            searchCustomer,
            clearSearch,
            loading,
            success,
            smsError,
            resultMessage
        }
    },
}
</script>


<style scoped>
    .table-scroll{
        overflow: scroll;
        height: 500px;
    }

    ::-webkit-scrollbar{
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        border-radius: 50px;
    }

    ::-webkit-scrollbar-thumb {
        background-color: rgb(109, 155, 255);
        border-radius: 5px;
    }

     ::-webkit-scrollbar-thumb:hover {
        background-color: rgb(182, 215, 255);
    }

    .clear {
        position: relative;
        right: 35px;
        color: darkblue;
        margin-top: 2px;
        z-index: 4;    
    }    

    .section-height{
        height: 80px;        
    }

</style>