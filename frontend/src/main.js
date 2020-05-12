import Vue from 'vue'
import VueRouter from 'vue-router'
import VModal from 'vue-js-modal'
import LightBootstrap from './light-bootstrap-main'
import axiosAuth from '@/api/axios-auth'
import axios from 'axios'
import store from '../store/index'


// Plugins
import App from './App.vue'

// router setup
import routes from './routes/routes'

axios.defaults.baseURL = 'http://localhost:5000';

// plugin setup
Vue.use(VueRouter)
Vue.use(LightBootstrap)
Vue.use(VModal, { dynamic: true, injectModalsContainer: true })

import VueYouTubeEmbed from 'vue-youtube-embed'
Vue.use(VueYouTubeEmbed)

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: 'active'
})

router.beforeEach((to, from, next) => {
	let token = localStorage.getItem('token');
	let requireAuth = to.matched.some(record => record.meta.requiresAuth);

	if (!requireAuth) {
		next();
	}

	if (requireAuth && !token) {
		next('/login');
	}

	if (to.path === '/login') {
		if (token) {
			axiosAuth.post('/verify-token').then(() => {
				next('/');
			}).catch(() => {
				next();
			});
		}
		else {
			next();
		}
	}

	if (to.path === '/register') {
		if (token) {
			axiosAuth.post('/verify-token').then(() => {
				next('/');
			}).catch(() => {
				next();
			});
		}
		else {
			next();
		}
	}


	if (requireAuth && token) {
		axiosAuth.post('/verify-token').then(() => {
			next();
		}).catch(() => {
			next('/login');
		})
	}
});


/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router: router,
  store: store
})

