import Vue from 'vue'
import VueRouter from 'vue-router'

const DashboardLayout = () => import('../containers/DashboardLayout.vue')


let dashboardView = {
  path: '/',
  name: 'Dashboard',
  component: DashboardLayout
}

Vue.use(VueRouter)
const routes = [
  dashboardView
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
