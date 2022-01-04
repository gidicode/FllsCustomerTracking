import { createApp, h, } from 'vue'
import App from './App.vue'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import router from './router'
import store from "./store"
import { provideApolloClient} from '@vue/apollo-composable'
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core'
import { onError } from '@apollo/client/link/error'
import { logErrorMessages } from '@vue/apollo-util'

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
    cache, link:errorlink.concat(link)
})

export const theClient = apolloClient

createApp({ App, setup() {
    provideApolloClient(apolloClient)
    },
    render() {
        return h(App)
    }
})
.use(router)
.use(store)
.mount('#app')
