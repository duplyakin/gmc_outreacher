const DashboardLayout = () => import('src/pages/Dashboard/Layout/DashboardLayout.vue')
//import DashboardLayout from 'src/pages/Dashboard/Layout/DashboardLayout.vue'

// GeneralViews
const NotFound = () => import('src/pages/GeneralViews/NotFoundPage.vue')

const Login = () => import('src/pages/Dashboard/Auth/login.vue')
const Register = () => import('src/pages/Dashboard/Auth/register.vue')

//Videos
const Videos = () => import('src/pages/Dashboard/Videos/trim_video.vue')
const PersVideos = () => import('src/pages/Dashboard/Videos/personalize_video.vue')
const PersGif = () => import('src/pages/Dashboard/Videos/personalize_gif.vue')
const PersLp = () => import('src/pages/Dashboard/Videos/personalize_lp.vue')
const PersPreview = () => import('src/pages/Dashboard/Videos/preview.vue')

//CUSTOM components created by me
const Profile = () => import('src/pages/Dashboard/Profile/profile.vue')
//const Profile = () => import('src/pages/Dashboard/Profile/1.vue') // test file
const Blacklist = () => import('src/pages/Dashboard/Blacklist/blacklist.vue')
const Subscription = () => import('src/pages/Dashboard/Subscription/subscription.vue')

const Dashboard = () => import('src/pages/Dashboard/Overview/Dashboard.vue')
const Help = () => import('src/pages/Dashboard/Overview/help.vue')

const Prospects = () => import('src/pages/Dashboard/Prospects/prospects.vue')
const ProspectLists = () => import('src/pages/Dashboard/ProspectLists/lists.vue')

// ---Campaigns---
const CampaignsList = () => import('src/pages/Dashboard/CampaignsList/campaigns.vue')

const CampaignFormStart = () => import('src/pages/Dashboard/CampaignsList/campaign_form_start.vue')

const CampaignFormType = () => import('src/pages/Dashboard/CampaignsList/campaign_form_type.vue')
const CampaignFormLeads = () => import('src/pages/Dashboard/CampaignsList/campaign_form_leads.vue')
const CampaignFormSequence = () => import('src/pages/Dashboard/CampaignsList/campaign_form_sequence.vue')
const CampaignFormAccounts = () => import('src/pages/Dashboard/CampaignsList/campaign_form_accounts.vue')
const CampaignFormSettings = () => import('src/pages/Dashboard/CampaignsList/campaign_form_settings.vue')

const CampaignForm = () => import('src/pages/Dashboard/CampaignsList/campaign_form.vue')

const CampaignEditForm = () => import('src/pages/Dashboard/CampaignsList/campaign_edit_form.vue')
const CampaignStatistic = () => import('src/pages/Dashboard/CampaignsList/campaign_statistic.vue')
// --------------

// ---Linkedin---
const CampaignDataFormType = () => import('src/pages/Dashboard/LinkedinActions/campaign_data_form_type.vue')

// search
const CampaignDataFormLeads = () => import('src/pages/Dashboard/LinkedinActions/search/campaign_data_form_leads.vue')
const CampaignDataFormSequence = () => import('src/pages/Dashboard/LinkedinActions/search/campaign_data_form_sequence.vue')
const CampaignDataFormAccounts = () => import('src/pages/Dashboard/LinkedinActions/search/campaign_data_form_accounts.vue')
const CampaignDataFormSettings = () => import('src/pages/Dashboard/LinkedinActions/search/campaign_data_form_settings.vue')

// SN search
const CampaignDataFormSNLeads = () => import('src/pages/Dashboard/LinkedinActions/search_sn/campaign_data_form_leads.vue')
const CampaignDataFormSNSequence = () => import('src/pages/Dashboard/LinkedinActions/search_sn/campaign_data_form_sequence.vue')
const CampaignDataFormSNAccounts = () => import('src/pages/Dashboard/LinkedinActions/search_sn/campaign_data_form_accounts.vue')
const CampaignDataFormSNSettings = () => import('src/pages/Dashboard/LinkedinActions/search_sn/campaign_data_form_settings.vue')

// post
const CampaignDataFormPostLeads = () => import('src/pages/Dashboard/LinkedinActions/post/campaign_data_form_leads.vue')
const CampaignDataFormPostSequence = () => import('src/pages/Dashboard/LinkedinActions/post/campaign_data_form_sequence.vue')
const CampaignDataFormPostAccounts = () => import('src/pages/Dashboard/LinkedinActions/post/campaign_data_form_accounts.vue')
const CampaignDataFormPostSettings = () => import('src/pages/Dashboard/LinkedinActions/post/campaign_data_form_settings.vue')

// old
const LinkedinEnrichment = () => import('src/pages/Dashboard/LinkedinActions/linkedin_enrichment.vue')
const LinkedinParsing = () => import('src/pages/Dashboard/LinkedinActions/linkedin_parsing.vue')
const LinkedinEnrichmentData = () => import('src/pages/Dashboard/LinkedinActions/linkedin_enrichment_data.vue')
// --------------

const Statistics = () => import('src/pages/Dashboard/Statistics/statistics.vue')
const Statistics_detailed = () => import('src/pages/Dashboard/Statistics/statistics_detailed.vue')

const Accounts = () => import('src/pages/Dashboard/Accounts/accounts.vue')
const Team = () => import('src/pages/Dashboard/Team/team.vue')

// admin
const Actions = () => import('src/pages/Dashboard/Actions/actions.vue')
const UsersList = () => import('src/pages/Dashboard/Admin/users_list.vue')
const GoogleAppSettings = () => import('src/pages/Dashboard/Admin/google_app_settings.vue')
const GoogleAppSettingsAdd = () => import('src/pages/Dashboard/Admin/google_app_settings_add.vue')
const Limits = () => import('src/pages/Dashboard/Admin/limits.vue')



let loginPage = {
  path: '/login',
  name: 'Login',
  component: Login
}

let registerPage = {
  path: '/register',
  name: 'Register',
  component: Register
}

let loginAdminPage = {
  path: '/admin/login',
  name: 'Login',
  redirect: '/login',
  component: Login
}

let adminMenu = {
  path: '/admin',
  component: DashboardLayout,
  redirect: '/admin/users_list',
 // meta: { requiresAuth: true, requiresAdmin: true },
  children: [
    {
      path: 'users_list',
      name: 'Users List',
      component: UsersList
    },
    {
      path: 'google_app_settings',
      name: 'Google App Settings',
      component: GoogleAppSettings
    },
    {
      path: 'google_app_settings_add',
      name: 'Google App Settings',
      component: GoogleAppSettingsAdd
    },
    {
      path: 'limits',
      name: 'Limits',
      component: Limits
    },
  ]
}

const routes = [
  loginPage,
  registerPage,
  adminMenu,
  loginAdminPage,
  {
   // meta: { requiresAuth: true, role: 'user' },
    path: '/',
    component: DashboardLayout,
    redirect: '/profile',
    children: [
      {
        path: 'profile',
        name: 'Profile',
        component: Profile
      },
      {
        path: 'blacklist',
        name: 'Blacklist',
        component: Blacklist
      },
      {
        path: 'subscription',
        name: 'Subscription',
        component: Subscription
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'help',
        name: 'Help',
        component: Help
      },
      {
        path: 'videos',
        name: 'Videos',
        component: Videos
      },
      {
        path: 'personalize_video',
        name: 'PersonalizeVideos',
        component: PersVideos
      },
      {
        path: 'personalize_gif',
        name: 'PersonalizeGif',
        component: PersGif
      },
      {
        path: 'personalize_preview',
        name: 'PersonalizePreview',
        component: PersPreview
      },
      {
        path: 'personalize_lp',
        name: 'PersonalizeLp',
        component: PersLp
      },

      {
        path: 'prospects',
        name: 'Leads',
        component: Prospects
      },
      {
        path: 'prospects_list',
        name: 'Leads Lists',
        component: ProspectLists
      },

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
        name: 'Sequences',
        component: CampaignsList
      },
      {
        path: 'campaign_form_sequence',
        name: 'New Campaign',
        component: CampaignFormSequence
      },
      {
        path: 'campaign_form_accounts',
        name: 'New Campaign',
        component: CampaignFormAccounts
      },
      {
        path: 'campaign_form_leads',
        name: 'New Campaign',
        component: CampaignFormLeads
      },
      {
        path: 'campaign_form_settings',
        name: 'New Campaign',
        component: CampaignFormSettings
      },
      {
        path: 'campaign_form',
        name: 'New Campaign',
        component: CampaignForm
      },
      {
        path: 'campaign_edit_form',
        name: 'Edit Campaign',
        component: CampaignEditForm
      },
      {
        path: 'campaign_statistic',
        name: 'Campaign Statistic',
        component: CampaignStatistic
      },

      {
        path: 'campaign_data_form_type',
        name: 'New Campaign',
        component: CampaignDataFormType
      },
      {
        path: 'campaign_data_form_sequence',
        name: 'New Campaign',
        component: CampaignDataFormSequence
      },
      {
        path: 'campaign_data_form_accounts',
        name: 'New Campaign',
        component: CampaignDataFormAccounts
      },
      {
        path: 'campaign_data_form_leads',
        name: 'New Campaign',
        component: CampaignDataFormLeads
      },
      {
        path: 'campaign_data_form_settings',
        name: 'New Campaign',
        component: CampaignDataFormSettings
      },

      {
        path: 'campaign_data_form_sn_sequence',
        name: 'New Campaign',
        component: CampaignDataFormSNSequence
      },
      {
        path: 'campaign_data_form_sn_accounts',
        name: 'New Campaign',
        component: CampaignDataFormSNAccounts
      },
      {
        path: 'campaign_data_form_sn_leads',
        name: 'New Campaign',
        component: CampaignDataFormSNLeads
      },
      {
        path: 'campaign_data_form_sn_settings',
        name: 'New Campaign',
        component: CampaignDataFormSNSettings
      },

      {
        path: 'campaign_data_form_post_sequence',
        name: 'New Campaign',
        component: CampaignDataFormPostSequence
      },
      {
        path: 'campaign_data_form_post_accounts',
        name: 'New Campaign',
        component: CampaignDataFormPostAccounts
      },
      {
        path: 'campaign_data_form_post_leads',
        name: 'New Campaign',
        component: CampaignDataFormPostLeads
      },
      {
        path: 'campaign_data_form_post_settings',
        name: 'New Campaign',
        component: CampaignDataFormPostSettings
      },

      {
        path: 'linkedin_enrichment',
        name: 'Leads managment',
        component: LinkedinEnrichment
      },
      {
        path: 'linkedin_parsing',
        name: 'Campaign Linkedin Parsing',
        component: LinkedinParsing
      },
      {
        path: 'linkedin_enrichment_data',
        name: 'Campaign Linkedin Enrichment Data',
        component: LinkedinEnrichmentData
      },

      {
        path: 'accounts',
        name: 'Accounts',
        component: Accounts
      },
      {
        path: 'team',
        name: 'Team',
        component: Team
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: Statistics
      },
      {
        path: 'statistics_detailed',
        name: 'Statistics detailed',
        component: Statistics_detailed
      }
    ]
  },
  {
    path: '/admin',
    component: DashboardLayout,
    //meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'actions',
        name: 'Actions',
        component: Actions
      },
    ]
  },
  {path: '*', component: NotFound},
]

export default routes
