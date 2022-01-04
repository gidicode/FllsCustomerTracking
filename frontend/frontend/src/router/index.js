import {createRouter, createWebHistory } from "vue-router"
import Dashboard from '../views/Dashboard/Dashboard.vue'
import CreateEntries from '../views/Dashboard/CreateEntriesForm.vue'
import LoginPage from '../views/components/LoginPage.vue'
import store from '../store'

const routes = [
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true},
        children: [
            {
                path: 'createEntries',
                component: CreateEntries,

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