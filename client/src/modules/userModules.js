import axios from 'axios'
import router from '@/router'
import actionHandler from '../utils/actionHandler'

const initialUserState = () =>
(JSON.parse(localStorage.getItem('user')) ?? {
    _id: '',
    name: '',
    email: '',
    isAdmin: false,
    createdAt: '',
    token: null
})

const state = {
    loggedUser: initialUserState(),
    userDetails: {},
    users: []
}

const getters = {
    getLoggedUser: state => state.loggedUser,
    getUserDetails: state => state.userDetails,
    getAllUsers: state => state.users
}

const actions = {
    loginUser: actionHandler(async ({ commit }, { email, password }) => {
        const { data } = await axios.post(
            '/api/users/login/',
            { 'username': email, 'password': password },
        )

        localStorage.setItem('user', JSON.stringify(data.data))
        commit('setUser', { user: data.data, statePiece: 'loggedUser' })
    }),
    logoutUser({ commit }) {
        localStorage.removeItem('user')
        commit('resetLoggedUser')

        router.push({
            name: 'login', query: {
                redirect: router.currentRoute.value.fullPath.slice(1)
            }
        })
    },
    registerUser: actionHandler(async ({ commit }, { name, email, password }) => {
        const { data } = await axios.post(
            '/api/users/register/',
            { 'name': name, 'email': email, 'password': password },
        )

        localStorage.setItem('user', JSON.stringify(data.data))
        commit('setUser', { user: data.data, statePiece: 'loggedUser' })
    }),
    fetchUserDetails: actionHandler(async ({ commit, state }, id) => {
        commit('resetUserDetails')

        const { data } = await axios.get(`/api/users/${id}`, {
            headers: { Authorization: `Bearer ${state.loggedUser.token}` }
        })

        commit('setUser', { user: data.data, statePiece: 'userDetails' })
    }),
    updateUserProfile: actionHandler(async ({ commit, state }, user) => {
        const { data } = await axios.put(`/api/users/profile/update/`,
            user,
            { headers: { Authorization: `Bearer ${state.loggedUser.token}` } }
        )

        localStorage.setItem('user', JSON.stringify(data.data))
        commit('setUser', { user: data.data, statePiece: 'loggedUser' })
    }),
    fetchAllUsers: actionHandler(async ({ commit, state }) => {
        commit('resetAllUsers')

        const { data } = await axios.get('/api/users/', {
            headers: { Authorization: `Bearer ${state.loggedUser.token}` }
        })

        commit('setAllUsers', data.data)
    }),
    deleteUser: actionHandler(async ({ dispatch, state }, userId) => {
        await axios.delete(`/api/users/delete/${userId}/`, {
            headers: { Authorization: `Bearer ${state.loggedUser.token}` }
        })

        dispatch('fetchAllUsers')
    }),
    updateUserDetails: actionHandler(async ({ commit, state }, user) => {
        const { data } = await axios.put(`/api/users/update/${user._id}/`,
            user,
            { headers: { Authorization: `Bearer ${state.loggedUser.token}` } }
        )

        commit('resetUserDetails')
        commit('setUser', { user: data.data, statePiece: 'userDetails' })
    })
}

const mutations = {
    resetLoggedUser: state => state.loggedUser = initialUserState(),
    resetUserDetails: state => state.userDetails = {},
    
    setUser: (state, { user, statePiece }) => Object.keys(user).forEach(key => state[statePiece][key] = user[key]),

    resetAllUsers: state => state.users = [],
    setAllUsers: (state, users) => state.users = users
}

export default {
    state,
    getters,
    actions,
    mutations
}