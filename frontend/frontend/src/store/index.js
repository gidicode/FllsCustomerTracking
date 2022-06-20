import { createStore } from 'vuex'
import AuthService from '../services/auth.service';
const user = window.localStorage.getItem("token")
const authenticated = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };  

const store = createStore({
    state () {
        return {
           authenticated,
           searchNameNumer: '',                      
           recordDetailsState: false,
           recordsHeadingState: true,
           editRecordState: false,
           personalSms:false,
           customerId: '',           
           canEdit: true,
           deletePageState: false,
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
           console.log('logging')
        },

        registerSuccess(state){
            state.authenticated.status.loggedIn = false
        },

        registerFailure(state) {
            state.authenticated.status.loggedIn = false
        },

        pushNumber (state, payload) {
            state.searchNameNumer = payload
        },

        openRecordDetails (state) {
            state.recordDetailsState = true
        },

        closeRecordDetails (state) {
            state.recordDetailsState = false
        },

        openEditRecord (state) {
            state.editRecordState = !state.editRecordState
        },

        getId (state, payload) {
            state.customerId = payload
        },

        hideRecordHeading (state) {
            state.recordsHeadingState = false
        },

        showRecordHeading (state) {
            state.recordsHeadingState = true
        },

        canEditCustomer (state) {
            state.canEdit = !state.canEdit
        },

        showPersonalSms (state) {
            state.personalSms = true
        },

        closePersonalSms (state) {
            state.personalSms = false
        },

        showDeletePage(state) {
            state.deletePageState = true
        },

        closeDeletePage(state) {
            state.deletePageState = false
        }
        
    }

})

export default store