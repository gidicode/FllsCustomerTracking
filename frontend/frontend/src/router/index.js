import {createRouter, createWebHistory } from "vue-router"
import Dashboard from '../views/Dashboard/Dashboard.vue'
import CreateEntries from '../views/Dashboard/CreateEntriesForm.vue'
import CreateRiders from '../views/Dashboard/CreateRiders.vue'
import Riders from '../views/Dashboard/Riders.vue'
import LoginPage from '../views/components/LoginPage.vue'
import SingleSms from '../views/components/SingleSms.vue'
import RidersDetails from '../views/components/RidersDetails.vue'
import EditRecords from '../views/components/Records/EditRecords.vue'
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
                            return { ...route.params }
                        },
                        meta: { requiresAuth: true }
                    },

                    {
                        path: 'editRecord/:id',
                        name: 'EditRecord',
                        component: EditRecords,                       
                        meta: { requiresAuth: true }
                    },

                    {
                        path: 'singleSms/:id',
                        name: 'SingleSms',
                        component: SingleSms,
                        meta: { requiresAuth: true},
                    }
                ]
            },            

            {
                path: 'Riders',
                name: 'Riders',
                component: Riders,
                meta: { requiresAuth: true },
                children: [
                    {
                        path: 'RidersDetails/:name',
                        name: 'RidersDetails',
                        component: RidersDetails,
                        props: (route) => {                            
                            return { ...route.params }
                        },
                        meta: { requiresAuth: true }
                    }
                ],
            }
        
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