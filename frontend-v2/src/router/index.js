import Vue from 'vue'
import VueRouter from 'vue-router'

const DashboardLayout = () => import('../containers/DashboardLayout.vue')

// ---Campaigns---
const CampaignsList = () => import('@/views/Campaigns/campaigns.vue')

const CampaignFormStart = () => import('@/views/Campaigns/campaign_form_start.vue')

const CampaignFormType = () => import('@/views/Campaigns/campaign_form_type.vue')
const CampaignFormLeads = () => import('@/views/Campaigns/campaign_form_leads.vue')
const CampaignFormSequence = () => import('@/views/Campaigns/campaign_form_sequence.vue')
const CampaignFormAccounts = () => import('@/views/Campaigns/campaign_form_accounts.vue')
const CampaignFormSettings = () => import('@/views/Campaigns/campaign_form_settings.vue')

//const CampaignStatistic = () => import('@/views/Campaigns/campaign_statistic.vue')
// --------------


let dashboardView = {
  path: '/',
  name: 'Dashboard',
  component: DashboardLayout
}

let campaigns = {
  //meta: { requiresAuth: true, role: 'user' },
  path: '/',
  component: DashboardLayout,
  //redirect: '/profile',
  children: [
    {
      path: 'campaign_form_start',
      name: 'New Campaign',
      component: CampaignFormStart
    },
    {
      path: 'campaign_form_type',
      name: 'New Campaign',
      component: CampaignFormType
    },
    {
      path: 'campaigns',
      name: 'Campaigns',
      component: CampaignsList
    },
    {
      path: 'campaign_form_sequence',
      name: 'Campaign Sequence',
      component: CampaignFormSequence
    },
    {
      path: 'campaign_form_accounts',
      name: 'Campaign Accounts',
      component: CampaignFormAccounts
    },
    {
      path: 'campaign_form_leads',
      name: 'Campaign Leads',
      component: CampaignFormLeads
    },
    {
      path: 'campaign_form_settings',
      name: 'Campaign Settings',
      component: CampaignFormSettings
    },
  ]
}

Vue.use(VueRouter)
const routes = [
  dashboardView,
  campaigns,
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
