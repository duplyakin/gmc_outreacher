const DashboardLayout = () => import('src/pages/Dashboard/Layout/DashboardLayout.vue')
//import DashboardLayout from 'src/pages/Dashboard/Layout/DashboardLayout.vue'
// GeneralViews
const NotFound = () => import('src/pages/GeneralViews/NotFoundPage.vue')

const Login = () => import('src/pages/Dashboard/Auth/login.vue')
const Register = () => import('src/pages/Dashboard/Auth/register.vue')

//CUSTOM components created by me
const Profile = () => import('src/pages/Dashboard/Profile/profile.vue')
//const Profile = () => import('src/pages/Dashboard/Profile/1.vue') // test file
const Blacklist = () => import('src/pages/Dashboard/Blacklist/blacklist.vue')
const Dashboard = () => import('src/pages/Dashboard/Overview/Dashboard.vue')
const Help = () => import('src/pages/Dashboard/Overview/help.vue')

const Prospects = () => import('src/pages/Dashboard/Prospects/prospects.vue')

const CampaignsList = () => import('src/pages/Dashboard/CampaignsList/campaigns.vue')
const CampaignForm = () => import('src/pages/Dashboard/CampaignsList/campaign_form.vue')
const CampaignEditForm = () => import('src/pages/Dashboard/CampaignsList/campaign_edit_form.vue')

const LinkedinEnrichment = () => import('src/pages/Dashboard/LinkedinActions/linkedin_enrichment.vue')
const LinkedinParsing = () => import('src/pages/Dashboard/LinkedinActions/linkedin_parsing.vue')
const LinkedinEnrichmentData = () => import('src/pages/Dashboard/LinkedinActions/linkedin_enrichment_data.vue')

const ProspectLists = () => import('src/pages/Dashboard/ProspectLists/lists.vue')


const Statistics = () => import('src/pages/Dashboard/Statistics/statistics.vue')
const Statistics_detailed = () => import('src/pages/Dashboard/Statistics/statistics_detailed.vue')

const Accounts = () => import('src/pages/Dashboard/Accounts/accounts.vue')
const Team = () => import('src/pages/Dashboard/Team/team.vue')
const Actions = () => import('src/pages/Dashboard/Actions/actions.vue')

// admin
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
  meta: { requiresAuth: true, requiresAdmin: true },
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
    meta: { requiresAuth: true, role: 'user' },
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
        path: 'campaigns',
        name: 'Sequences',
        component: CampaignsList
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
    meta: { requiresAuth: true, requiresAdmin: true },
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
