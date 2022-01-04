import gql from "graphql-tag"
import { useQuery, useResult} from '@vue/apollo-composable'
import { provideApolloClient} from '@vue/apollo-composable'
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core'

const Headers = () => {
    const headers = {}
    const token = window.localStorage.getItem("token")

    if (token) {        
        headers.authorization = `jwt ${token}`
    }
    return headers
}

const cache = new  InMemoryCache()
const link = createHttpLink({
    uri: 'http://localhost:8000/graphql',
    fetch,
    headers: Headers()
})
const apolloClient  = new ApolloClient({   
    cache, link
})
provideApolloClient(apolloClient)


const { result:GetRider } = useQuery(gql`
    query  GetRider {
        ridersList{
            id
            riderName
            riderNumber
        }
    }
`)

export const GetRiders = useResult(GetRider)

