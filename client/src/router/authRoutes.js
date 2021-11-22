export default [
    {
        path: '/login',
        name: 'login',
        component: () => import(/* webpackChunkName: "login-view" */ '@/views/Auth/Login.vue')
    },
    {
        path: '/register',
        name: 'register',
        component: () => import(/* webpackChunkName: "register-view" */ '@/views/Auth/Register.vue')
    },
]