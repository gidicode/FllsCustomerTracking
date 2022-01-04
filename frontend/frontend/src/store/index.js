import { createStore } from 'vuex'
import AuthService from '../services/auth.service';

/*const store = createStore({
    modules:{
        auth, 
    }
})*/
const user = window.localStorage.getItem("token")
const authenticated = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };


const store = createStore({
    state () {
        return {
           authenticated
        }
    },

    actions: {
        loginSuccess: ({ commit }) => commit ('loginSuccess'),
        loggedInFailure: ({ commit }) => commit ('loggedInFailure'),
        logout ({ commit }) {
            AuthService.logout(),
            commit('logout') 
        },  
        registerSuccess: ({ commit }) => commit('registerSuccess'),
        registerFailure: ({ commit }) => commit('registerFailure'),
    },

    mutations: {
        loginSuccess(state, user) {
            state.authenticated.status.loggedIn = true
            state.authenticated.user = user
        },
    
        loggedInFailure(state) {
            state.authenticated.status.loggedIn = false
            state.authenticated.user = null
        },
    
        logout(state) {
           state.authenticated.status.loggedIn = false
           state.authenticated.user = null
        },

        registerSuccess(state){
            state.authenticated.status.loggedIn = false
        },

        registerFailure(state) {
            state.authenticated.status.loggedIn = false
        }
    }

})

export default store
