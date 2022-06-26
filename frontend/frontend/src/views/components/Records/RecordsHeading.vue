<template>
    <section class="shadow-sm the-section">        
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
                    <strong> Unique:</strong> <br> {{ UniqueEntriesLength.length }}
                </p>                                                                         
            </div>

            <div class="p-2 bd-highlight">                                               
                <p class="lh-1" >
                    <strong>Total</strong> <br> {{ EntriesLength }}
                </p>    
            </div>            
        </div>               
    </section>
</template>

<script>
import {toRef} from '@vue/reactivity'
export default {
    name: 'RecordsHeading',
    props: {
        allEntries: Object,
        allCustomers: Object,
    },

    setup(props) {
        const EntriesLength = toRef(props, 'allEntries')
        const UniqueEntriesLength = toRef(props, 'allCustomers')                

        return {
            EntriesLength,
            UniqueEntriesLength
        }
    }
}
</script>

<style scoped>
.the-section{
    background-color: rgb(16, 0, 61);    
    padding: 15px;
    height: 4.6rem;
}

.icon{
    background-color: #6e9fdf;
}
</style>