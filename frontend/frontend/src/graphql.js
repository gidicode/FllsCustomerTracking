import gql from "graphql-tag"
import { useQuery, useResult} from '@vue/apollo-composable'
import { provideApolloClient} from '@vue/apollo-composable'
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core'
import { logErrorMessages } from '@vue/apollo-util'
import { onError } from '@apollo/client/link/error'

const errorlink = onError(error => {
    logErrorMessages(error)
  })

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
    cache, link: errorlink.concat(link)
})
provideApolloClient(apolloClient)


const { result: GetRider } = useQuery(gql`
    query  GetRider {
        ridersList{
            id
            riderName
            riderNumber
        }
    }
`)


const { result: EntriesToday } = useQuery(gql`
        query singleEntries {
            entriesTodaySingle{
                id
                customerName
                customerContact
            },
            
            entriesTodayMultiple{
                id
                customer {
                    customerName
                    customerContact
                }
            }
        }
`)

export const GetRiders = useResult(GetRider)
export const singleEntriesToday = useResult( EntriesToday, [], data => data.entriesTodaySingle )
export const multipleEntriesToday = useResult( EntriesToday, [], data => data.entriesTodayMultiple)
export const riderQuery = EntriesToday