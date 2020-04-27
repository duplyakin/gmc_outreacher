import Vue from 'vue'
import VueRouter from 'vue-router'
import VModal from 'vue-js-modal'
import LightBootstrap from './light-bootstrap-main'

import Vuex from "vuex"

// Plugins
import App from './App.vue'

// router setup
import routes from './routes/routes'
// plugin setup
Vue.use(VueRouter)
Vue.use(LightBootstrap)
Vue.use(VModal, { dynamic: true, injectModalsContainer: true })
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    campaign: {
      name: '',
      funnel: '',
      account: '',
      prospectsList: '',
      messagesList: [],
      timeTable: {
        from: '',
        till: '',
        timezone: '',
        days: [],
      },
    },
  },
  getters: {},
  mutations: {
    step_0 (state, data) {
      state.campaign.name = data.name;
      state.campaign.funnel = data.funnel;
    },
    step_1 (state, data) {
      state.campaign.account = data.account;
      state.campaign.prospectsList = data.prospectsList;
    },
    step_2 (state, data) {
      state.campaign.messagesList = data;
      //console.log('messagesList: ', state.campaign.messagesList);
    },
    step_3 (state, data) {
      state.campaign.timeTable = data;
    }
  },
  actions: {}
 })

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: 'active'
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
})

