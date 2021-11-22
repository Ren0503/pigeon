import { createStore } from 'vuex'

import users from '../modules/userModules'
import utils from '../modules/utilModules'

export default createStore({
    modules: {
        users,
        utils,
    }
})