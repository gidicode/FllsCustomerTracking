<template>
    <div class="container login">
        <div class="row">
            <div class="col-md-3">                
                
            </div>
            <div class="col-md-6">
                
                <section class="bg-light shadow-sm p-4 text-start changeFormWidth"> 
                    <h1 class="theText text-center text-primary font-weight-bold mt-4"> C-Track</h1>                   
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
                        <button type="submit" class="btn btn-primary w-100 mb-4">Login</button>

                        <p class="text-end">Forgot password? <span>Recover</span></p>
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
            path: '/dashboard/records',
        })
    }
    function redirectTologin() {
        router.push({
            name: 'Login',
        })
    }

    onMounted(() => {
        console.log('GetState',getState.value.status.loggedIn)
        if (getState.value.status.loggedIn) {
            redirectToDashboard() 
        }

        else {
            redirectTologin()
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
                console.log('Dara',data)
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


.login{
    margin-top: 10%;
}
</style>