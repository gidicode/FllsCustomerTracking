<template>
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <h5 class="theText1 text-start">First Laurel Logistics Services</h5>
                <h3 class="theText text-start text-primary font-weight-bold"> Customer Tracking Page</h3>
            </div>
            <div class="col-md-6">
                
                <section class="bg-light shadow-sm p-3 text-start changeFormWidth">                    
                    <p v-for="err in error" :key="err.code" class="text-danger">
                        {{ err.message}}
                    </p>
                   <form @submit.prevent="login">
                        <div class="mb-3">
                            <label for="InputEmail1" class="form-label theText">Email address</label>
                            <input type="email" class="form-control" id="InputEmail1" v-model="email" aria-describedby="emailHelp">                            
                        </div>
                        <div class="mb-3">
                            <label for="InputPassword1" class="form-label theText">Password</label>
                            <input type="password" class="form-control" v-model="password" id="InputPassword1">
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Submit</button>
                    </form>                    
                </section>
            </div>
            <div class="col-md-3">
                
            </div>
        </div>
    </div>        
</template>

<script>
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed, ref } from '@vue/reactivity'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { onMounted } from '@vue/runtime-core'

export default {

    name: 'LoginPage',
    setup() {
    
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const router = useRouter()        
    const store = useStore()

    const logInUser = () => store.dispatch('loginSuccess')
    const logoutUser = () => store.dispatch('logout')
    const getState = computed(() => store.state.authenticated)

    function redirectToDashboard() {
        router.push({
            name: 'Dashboard',
        })
    }
    function redirectTologin() {
        router.push({
            name: 'Login',
        })
    }

    onMounted(() => {
        if (getState.value.status) {
            redirectToDashboard() 
        }
    })
    
    const {mutate: login, onDone, loading:loginLoading } = useMutation(gql`
            mutation ( $email: String!, $password: String!){
                tokenAuth( email: $email, password: $password) {
                    token,
                    success,
                    errors,                    
                    user {
                        id,
                        email,
                    }   
                }
            }
        `, () => ({
            variables: {
                email: email.value,
                password: password.value
            },
            update: (cache, { data }) => {
                if (!data.tokenAuth.errors){
                    localStorage.setItem("token", data.tokenAuth.token)
                    logInUser()      
                    if (getState.value.status) {
                        redirectToDashboard()   
                    }else {
                        logoutUser()
                        redirectTologin()
                    }                                                                       
                }else {
                    let errors = []
                    for(let e of data.tokenAuth.errors.nonFieldErrors) {
                        errors.push(e)
                    }
                    error.value = errors
                }                                  
            }
        })
        )
        
    return {
        login,
        email,
        password, 
        loginLoading,
        onDone,
        error,        
    }
    },
}
</script>

<style scoped>
.theText {
    font-family: 'Comfortaa', cursive;
}

.theText1 {
    font-family: 'Comfortaa', cursive;
    font-weight: 800;
}

.changeFormWidth{
    width: 70%;
    margin-right: auto;
    margin-left: auto;
}
</style>