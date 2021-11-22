import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import auth from './authRoutes'

const routes = [
    ...auth,
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    scrollBehavior: () => ({ left: 0, top: 0 })
})

// Checking for logged user and for admin user
router.beforeEach((to, _, next) => {
    const user = (store.getters['getLoggedUser'])
    
    if (to.matched.some(route => route.meta.requiresAuth === true) && !user._id)
        next({ name: 'login', query: { redirect: to.fullPath.slice(1) } })
    
    else if (to.matched.some(route => route.meta.requiresAuth === 'Admin') && !user.isAdmin) next({ name: 'Home' })

    else next()
})

export default router