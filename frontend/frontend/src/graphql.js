import gql from "graphql-tag"
import { useQuery, useResult, provideApolloClient} from '@vue/apollo-composable'
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

const cache = new InMemoryCache()
const link = createHttpLink({
    uri: 'http://localhost:8000/graphql',
    fetch,
    headers: Headers()
})
const apolloClient  = new ApolloClient({   
    cache, 
    link: errorlink.concat(link),     
})
provideApolloClient(apolloClient)


export const GETRIDER  = gql`
    query  GETRIDER {
        ridersList{
            id
            riderName
            riderNumber
        }
    },    
`

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


export const ENTRIES = gql`
    query EntriesToday {
        entriesTodaySingle{
            id
            customerName
        }
    }
`

const { result: RecordList, loading } = useQuery(gql`
    query customerEntries {
        customerEntries {
            id
            customerName
            customerContact
            Rider {
                id
                riderName
                riderNumber
            }
            count {
                id
                customerContact
                dateCreated                
                discountAmount
                Rider{
                    id
                    riderName
                    riderNumber
                }
            }
            discountAmount
            dateCreated
        
        },

        relatedEnteries{
            id
            customer {
                id
                customerName
                customerContact
            }
            Rider {
                id
                riderName
            }
            customerContact
            discountAmount
            dateCreated            
        }
    }
`)

const { result: GetRidersQuery } = useQuery(GETRIDER)
export const GetRiders = useResult(GetRidersQuery, [])
export const singleEntriesToday = useResult( EntriesToday, [], data => data.entriesTodaySingle )
export const multipleEntriesToday = useResult( EntriesToday, [], data => data.entriesTodayMultiple)
export const RecordQueryUnique = useResult( RecordList, [], data => data.customerEntries)
export const RecordQueryMultiple = useResult( RecordList, [], data => data.relatedEnteries)
export const load = loading