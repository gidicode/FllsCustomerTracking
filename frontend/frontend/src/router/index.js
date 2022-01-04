import {createRouter, createWebHistory } from "vue-router"
import Dashboard from '../views/Dashboard.vue'
import LoginPage from '../components/LoginPage'

const routes = [
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true}
    },

    {
        path: '/login',
        redirect: 'Login',
        component: LoginPage,
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    linkActiveClass: 'active'
})

/*
router.beforeEach((to,) => {
    if(to.meta.requiresAuth && !store.state.authenticated){
        return {
            name:'Login',
        }
    }
})*/

export default router