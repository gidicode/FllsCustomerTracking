<template> 
 <main role="main" class="container-fluid">
    <div class="row">
        <div class="col-md-2 dashboard-body">
            <section class="text-left links" >
                
                <router-link to="/dashboard/createEntries">                                               
                    <section class="text-bak">                        
                        <div class="d-flex flex-row bd-highlight mb-3 background">
                            <div class="p-2 bd-highlight">
                                <h6><i class="fas fa-plus"></i></h6>
                            </div>                                  
                            <div class="p-2 bd-highlight">
                                <h6 role="button">Customers</h6>
                            </div>                            
                        </div>     
                    </section>
                </router-link>                                   

                <router-link to="/dashboard/records">
                    <section class="text-bak">  
                        <div class="d-flex flex-row bd-highlight mb-3 background">
                            <div class="p-2 bd-highlight">
                                <h6><i class="fas fa-list"></i></h6>
                            </div>
                            <div class="p-2 bd-highlight">
                                <h6 role="button">Records</h6>
                            </div>                            
                        </div>   
                    </section>
                    </router-link>

                <router-link to="/dashboard/createRiders">
                    <section class="text-bak ">  
                        <div class="d-flex flex-row bd-highlight mb-3 background">
                            <div class="p-2 bd-highlight">                               
                                <h6><i class="fas fa-plus"></i></h6>                                   
                            </div>
                            <div class="p-2 bd-highlight">
                                <h6 role="button">Add Riders</h6>
                            </div>                            
                        </div>                                                                                   
                    </section>
                </router-link>

                <router-link to="/dashboard/Riders">
                    <section class="text-bak">  
                        <div class="d-flex flex-row bd-highlight mb-3 background">
                            <div class="p-2 bd-highlight">
                                <h6><i class="fas fa-user-tie"></i></h6>
                            </div>
                            <div class="p-2 bd-highlight">
                                <h6 role="button">Riders</h6>
                            </div>                            
                        </div>                                                                                   
                    </section>
                </router-link>

                <router-link to="/dashboard/sendSms">
                    <section class="text-bak">  
                        <div class="d-flex flex-row bd-highlight mb-3 background">
                            <div class="p-2 bd-highlight">
                                <h6><i class="fas fa-sms"></i></h6>
                            </div>
                            <div class="p-2 bd-highlight">
                                <h6 role="button">Send Sms</h6>
                            </div>                            
                        </div>                                                                                   
                    </section>
                </router-link>
                
                <div class="d-flex flex-row bd-highlight mb-3 background log-out">
                    <div class="p-2 bd-highlight">
                        <h6><i class="fas fa-sign-out-alt"></i></h6>
                    </div>
                    <div class="p-2 bd-highlight">
                        <h6 role="button" @click="logoutUser()">Log Out</h6>                        
                    </div>                            
                </div>                                                                                   
                                    
            </section>
        </div>
        <div class="col-md-10 bg-light  ">                    
            <section class="the-body  mt-3">                                                
                <router-view/>                       
            </section>   
        </div>
    </div>      
 </main>  
</template>

<script>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
export default {
    name: "Dashboard",    

    setup() {
        const store = useStore()
        const router = useRouter()  
        
        const logoutUser = () => { 
            store.dispatch('logout')
            router.push({
            name: 'Login',
            })
        }                

        return {
            logoutUser,            
        }
    }
}

</script>
<style scoped>    
       
    .dashboard-body{
        background-color: rgb(16, 0, 61);                                                        
        min-height: 100vh;                        
        min-width: auto;
        overflow: hidden;
    }      

    .links{
        margin-top: 50%;
        color: white;        
        position: static;
    }
    
    h6{        
        font-family: 'Comfortaa', cursive;
        font-weight: 700;
        font-size: 17px;
    }   
    
    .background{
        margin-left: 30px;
        position: relative;
        top: 7px;
    } 

    .text-bak{
        min-width: 100vw;
    }

    .text-bak:hover{
        background-color: rgb(15, 45, 136);                    
        min-width: 100vw;
    }
 
    .top{
        background-color: white;
        box-shadow:  0px 4px 4px rgba(65, 9, 9, 0.08);
        width: auto;
        height: 100%;                
    }

    a {
        text-decoration: none;
        color: white;
    }

    .active .text-bak {        
        color: rgb(255, 255, 255);
        background-color: rgb(45, 93, 240);
        min-width: 100vw;
    }        

    .log-out{
        margin-top: 150px;
    }
  </style>


