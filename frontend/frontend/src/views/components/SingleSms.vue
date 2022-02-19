<template>
    <div>
        <button @click.self="sendEditModal()" type="button" class="btn-close close-button btn-light close-button " aria-label="Close"></button>        

        <div class="form-background">
            <p class="text-primary">Send SMS to this customer</p>
            <form @submit.prevent="editEntries()">               
                <div class="mb-3">
                    <label for="customerContact" class="form-label">Customer Phone</label>
                    <input type="text" class="form-control" id="customerContact" v-model= "customerNumber">
                    <span class="error-text"></span>
                </div>                

                <div>
                    <label for="smsBody" class="form-label"> Message Body</label>                    
                    <textarea name="smsBody" class="form-control" id="smsBody" cols="30" rows="10"></textarea>
                    <span class="error-text"></span>                
                </div>               
                
                <button class="btn btn-primary mt-4" type="button" disabled v-if="loading">
                    <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                    Sending...
                </button>  
                <button type="submit" class="btn btn-primary mt-4" v-else>Send</button>
                
            </form>      
        
            <div class="submitError" v-if="ErrorMessage">
                <h6 class="text-danger">an Error occured</h6>                            
            </div> 
        </div>
    </div>

</template>

<script>
import { computed } from '@vue/reactivity'
import { useRoute } from 'vue-router'

export default {
    name: 'SingleSms',
    emits: ['showEditModal'],

    setup(props, context) {
        const route = useRoute()
        const customerNumber = computed(() => route.params.customerContact)

        const sendEditModal = () => {
            context.emit('showEditModal')
        }

        return {
            sendEditModal,
            customerNumber
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