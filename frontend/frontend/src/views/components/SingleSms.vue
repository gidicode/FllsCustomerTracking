<template>
    <div>
        <button @click.self="sendEditModal()" type="button" class="btn-close close-button btn-light close-button " aria-label="Close"></button>        

        <div class="form-background">
            <p class="text-primary">Send SMS to this customer</p>
            <form @submit.prevent="onSubmit()">                               
                <div class="mb-3">
                    <label for="customerContact" class="form-label">Customer Phone</label>
                    <input type="text" class="form-control" id="customerContact" disabled v-model= "customerNumber">
                    <span class="error-text"></span>
                </div>                

                <div>
                    <label for="smsBody" class="form-label"> Message Body</label>                    
                    <textarea name="smsBody" class="form-control" id="smsBody" v-model="Message" cols="30" rows="10"></textarea>
                    <span class="error-text"></span> 
                </div>

                <button class="btn btn-primary mt-4" type="button" disabled v-if="loading">
                    <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                    Sending...
                </button>  

                <button type="submit" class="btn btn-primary mt-4" v-else>Send</button>

                <div class="success" v-if="success">
                    <p class="text-success">Sent Successfully</p> <font-awesome-icon icon="fa-solid fa-circle-check" />
                </div>

                <div class="error" v-if="smsError">
                    <p class="text-danger">An error occured</p> <font-awesome-icon icon="fa-solid fa-circle-check" />
                </div>

                <div class="submitError" v-if="MessageError">
                    <h6 class="text-danger"> Error ccured</h6>                            
                    {{ MessageError }}
                </div>                 
            </form>                  
        </div>
    </div>

</template>

<script>
import { computed, ref, toRef} from '@vue/reactivity'
import { useRoute } from 'vue-router'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import { watch } from '@vue/runtime-core'

export default {
    name: 'SingleSms',
    emits: ['showEditModal'],
    props: {
        uniqueCustomers: Object
    },

    setup(props, context) {
        const route = useRoute()
        const GetId = computed(() => route.params.id )
        const customerNumber = ref('')
        const getCustomerDetails = toRef(props, 'uniqueCustomers')

        watch(
            () => route.params.id,
            () => { filterContact }
        )

        const filterContact = computed(() => getCustomerDetails.value.filter (
            getCustomers => getCustomers.id == GetId.value
        ))
        filterContact.value.forEach(element => { customerNumber.value = element.customerContact})

        const schema = yup.object({
            Message: yup.string().required().max(200, 'Exceed message space'),
        })          
        useForm({
            validationSchema: schema,
        })
        const { handleSubmit } = useForm({
            validationSchema: schema,
        })            
        const { value: Message, errorMessage: MessageError } = useField('Message')        
        
        const sendEditModal = () => {
            context.emit('showEditModal')
        }
                             
        const GettingResult = ref('')

        const loading = ref(false)
        const success = ref(false)        
        const smsError = ref(false)

        const changeLoadingState = () => loading.value = !loading.value
        const changeSuccessState = () => success.value = !success.value
        const changeSmsErrorState = () => smsError.value = !smsError.value        
                 
        const onSubmit = handleSubmit(() => {                  
            changeLoadingState()           

           var raw = {
                "sender_name" : "FLLS",
                "message": '',
                "recipients": customerNumber.value,
            }

            raw.message = Message.value

            var requestOptions = {
                method: 'POST',
                body: JSON.stringify(raw),
                redirect: 'follow',
                headers: {
                    'Authorization': 'Bearer E9jriOUBg5ssOLSAc6DzE94O9cjxQ5kB6iW7DEv6mEADXs5Q2QcPXgOS0AVL',
                    'Content-Type' : 'application/json'                
                }}

                fetch("https://app.multitexter.com/v2/app/sendsms", requestOptions)
                .then(response => response.text())
                .then(result => {
                    GettingResult.value = JSON.parse(result)               
                    changeLoadingState()

                    if (GettingResult.value.status !== 1) {
                        smsError.value = true
                    }else if (GettingResult.value.status === 1 ) {
                        changeSuccessState()
                    }
                })
                .catch(error => {
                    if (error) {
                        changeSmsErrorState()
                        changeLoadingState()
                    }
                });
        })        

        return {
            sendEditModal,
            customerNumber,  
            onSubmit,         
            Message,
            MessageError,
            loading,
            success,
            smsError
        }
    },
}
</script>

<style scoped>
.close-button{
    background-color: white;
}

.form-background{
    width: 30%;
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin-right: auto;
    margin-left: auto;
    margin-top: 20px;    
}
</style>