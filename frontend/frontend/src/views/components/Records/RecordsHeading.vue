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
                <p class="lh-1" v-if="loading">
                    <strong> Calaculating....</strong>
                </p> 
                <p class="lh-1" v-else>
                    <strong> Unique:</strong> <br> {{ UniqueEntriesLength.length }}
                </p>                                                                         
            </div>

            <div class="p-2 bd-highlight">                                               
                <p class="lh-1" v-if="loading">
                   <strong> Calaculating....</strong>
                </p>   
                <p class="lh-1" v-else>
                    <strong>Multiple </strong> <br> {{ EntriesLength.length  }}
                </p>   
            </div>            
        </div>               
    </section>
</template>

<script>
import { RecordQueryUnique, RecordQueryMultiple, load} from '../../../graphql'
export default {
    name: 'RecordsHeading',   
    setup() {
        const EntriesLength =  RecordQueryMultiple
        const UniqueEntriesLength =  RecordQueryUnique            
        const loading = load

        console.log("Entries", EntriesLength.value.length)

        return {
            EntriesLength,
            UniqueEntriesLength,
            loading
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