import {createRouter, createWebHistory } from "vue-router"
import Dashboard from '../views/Dashboard/Dashboard.vue'
import CreateEntries from '../views/Dashboard/CreateEntriesForm.vue'
import CreateRiders from '../views/Dashboard/CreateRiders.vue'
import LoginPage from '../views/components/LoginPage.vue'
import Record from '../views/Dashboard/Records.vue'
import RecordDetails from '../views/components/Records/RecordsDetails.vue'
import store from '../store'

const routes = [
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true},
        props: true,
        children: [
            {
                path: 'createEntries',
                component: CreateEntries,
                meta: { requiresAuth: true },
            }, 
            
            {
                path: 'createRiders',
                component:CreateRiders,
                meta: { requiresAuth: true },
            },

            {
                path: 'records',
                component: Record,
                meta: { requiresAuth: true },
                props: true,
                children: [
                    {
                        path: 'recordDetails/:id',
                        name: 'RecordDetails',                        
                        component: RecordDetails,                        
                        props: (route) => {
                            console.log(route)
                            return { ...route.params }
                        },
                        meta: { requiresAuth: true }
                    },
                ]
            },            
        
        ]
    },

    {
        path: '/',
        name: 'Login',
        component: LoginPage,
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    linkActiveClass: 'active'
})

router.beforeEach((to) => {

    if(to.meta.requiresAuth && !store.state.authenticated){
        return {            
            name:'Login',
            query: {redirect: to.fullPath },
        }
    }
})

export default router