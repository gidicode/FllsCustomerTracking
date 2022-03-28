<template >    
    <div class="container-fluid">
        <div class="input-group">
            <span class="input-group-text icon" id="basic-addon1"><i class="fas fa-search text-white"></i></span>                     
            <input type="text" v-model="searchName" class="form-control" placeholder="Search..." aria-describedby="basic-addon1"/>
            <span class="clear btn btn-outline-dark" @click="clearSearch()">
                <i class="fas fa-times"></i></span>            
        </div>

        <div v-if="searchName.length > 0" class="mt-4">
            <ul v-for="items in searchedCustomers" :key="items.id">
                <li> {{ items.customerName}} {{ items.customerContact}}
                    <span @click="pushNumber(items.customerContact)" class="btn btn-sm btn-outline-success">Add</span>
                </li>
            </ul>
        </div>

        <p v-if="loading == true">
            loading....
        </p>

        
        
    </div>                    
</template>

<script>
import { computed, ref } from '@vue/reactivity'
import { RecordQueryUnique } from '../../graphql'
import { useStore } from 'vuex'
//import gql from "graphql-tag"
//import { useQuery } from '@vue/apollo-composable'

export default {
    name: 'EntriesToday',
    //props: ['type'],
    setup() {
        const store = useStore()
        const uniqueCustomers = computed(() => RecordQueryUnique.value)                

        const searchName = ref('')
        const searchedCustomers = computed(() => {
            return uniqueCustomers.value.filter((allCustomer) => {
                return (
                    allCustomer.customerName
                    .toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1 ||
                    allCustomer.customerContact
                    .toLowerCase()
                    .indexOf(searchName.value.toLowerCase()) != -1
                )  
            }) 
        })

        const clearSearch = () => searchName.value = ''

        const pushNumber = (item) => {
            store.commit('pushNumber', item)
        }

        //////////
        /*
        const {result, fetchMore, loading } = useQuery(FEED_QUERY, () => ({
            type: props.type,
            offset: 0,
            limit: 10,
        }))        
            
        function loadMore () {
            fetchMore({
                // note this is a different query than the one used in `useQuery`
                query: gql`
                query getMoreFeed ($cursor) {
                    moreFeed (type: $type, cursor: $cursor) {
                    cursor
                    posts {
                        id
                        # ...
                    }
                    }
                }
                `,
                variables: {
                cursor: result.feed.cursor,
                },
                updateQuery: (previousResult, { fetchMoreResult }) => {
                return {
                    ...previousResult,
                    feed: {
                    ...previousResult.feed,
                    // Update cursor
                    cursor: fetchMoreResult.moreFeed.cursor,
                    // Concat previous feed with new feed posts
                    posts: [
                        ...previousResult.feed.posts,
                        ...fetchMoreResult.moreFeed.posts,
                    ],
                    }
                }
                },
            })
        }*/

        return {
            uniqueCustomers,
            searchName, 
            searchedCustomers,
            clearSearch,
            pushNumber,
            //loadMore,
            //result,
            //loading
        }
    },
}
</script>

<style scoped>
    .changeText {
        font-size: 14px;
    }

    .title{
        background-color: rgb(207, 238, 177);
        padding: 5px;
        border-radius: 10px;        
        font-weight: 500;
    }

    h6 {
        font-family: 'Comfortaa', cursive;
    }

</style>