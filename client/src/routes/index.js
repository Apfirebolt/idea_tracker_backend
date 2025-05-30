import { createRouter, createWebHistory } from 'vue-router'
import Home from '../screens/Home.vue'
import Dashboard from '../screens/Dashboard.vue'
import NotFound from '../screens/404.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard
    },
    {
        path: '/explore',
        name: 'Explore',
        component: () => import('../screens/Explore.vue')
    },
    {
        path: '/ideas/:ideaId',
        name: 'IdeaDetail',
        component: () => import('../screens/IdeaDetail.vue')
    },
    {
        path: '/users/:userId',
        name: 'UserDetail',
        component: () => import('../screens/UserDetail.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../screens/Login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../screens/Register.vue')
    },
    {
        path: '/:catchAll(.*)',
        name: 'NotFound',
        component: NotFound
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router