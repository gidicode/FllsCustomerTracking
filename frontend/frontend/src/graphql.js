/*import gql from "graphql-tag"
import { provideApolloclient, useQuery, useResult} from '@vue/apollo-composable'
import { ApolloClient, InMemomryCache, createHttpLink } from '@apollo/client/core'
import { onError } from '@apollo/client/link/error'
import { logErrorMessages } from '@vue/apollo-util'

const errorlink = onError( error => {
    logErrorMessages(error)
})

const cache = new InMemomryCache()
const link = createHttpLink({ uri:'http://localhost:8000/graphql'})
const apolloClient = new ApolloClient({
    cache, link: errorlink.concat(link)
})
provideApolloclient(apolloClient)

const { result } = useQuery(gql`
    query 
`)
*/