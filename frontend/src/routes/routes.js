const DashboardLayout = () => import('src/pages/Dashboard/Layout/DashboardLayout.vue')
//import DashboardLayout from 'src/pages/Dashboard/Layout/DashboardLayout.vue'
// GeneralViews
const NotFound = () => import('src/pages/GeneralViews/NotFoundPage.vue')
// Dashboard pages
const Overview_standart = () => import('src/pages/Dashboard/Dashboard/Overview.vue')
const Stats = () => import('src/pages/Dashboard/Dashboard/Stats.vue')

// Pages
const User = () => import('src/pages/Dashboard/Pages/UserProfile.vue')
const TimeLine = () => import('src/pages/Dashboard/Pages/TimeLinePage.vue')
const Login = () => import('src/pages/Dashboard/Auth/login.vue')
const Register = () => import('src/pages/Dashboard/Auth/register.vue')

// Components pages
const Buttons = () => import('src/pages/Dashboard/Components/Buttons.vue')
const GridSystem = () => import('src/pages/Dashboard/Components/GridSystem.vue')
const Panels = () => import('src/pages/Dashboard/Components/Panels.vue')
const SweetAlert = () => import('src/pages/Dashboard/Components/SweetAlert.vue')
const Notifications = () => import('src/pages/Dashboard/Components/Notifications.vue')
const Icons = () => import('src/pages/Dashboard/Components/Icons.vue')
const Typography = () => import('src/pages/Dashboard/Components/Typography.vue')

// Forms pages
const RegularForms = () => import('src/pages/Dashboard/Forms/RegularForms.vue')
const ExtendedForms = () => import('src/pages/Dashboard/Forms/ExtendedForms.vue')
const ValidationForms = () => import('src/pages/Dashboard/Forms/ValidationForms.vue')
const Wizard = () => import('src/pages/Dashboard/Forms/Wizard.vue')

// TableList pages
const RegularTables = () => import('src/pages/Dashboard/Tables/RegularTables.vue')
const ExtendedTables = () => import('src/pages/Dashboard/Tables/ExtendedTables.vue')
const PaginatedTables = () => import('src/pages/Dashboard/Tables/PaginatedTables.vue')


// Charts
const Charts = () => import('src/pages/Dashboard/Charts.vue')



//CUSTOM components created by me
const Profile = () => import('src/pages/Dashboard/Profile/profile.vue')
const Overview = () => import('src/pages/Dashboard/Overview/Overview.vue')
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


let componentsMenu = {
  path: '/admin/components',
  component: DashboardLayout,
  redirect: '/components/buttons',
  children: [
    {
      path: 'buttons',
      name: 'Buttons',
      component: Buttons
    },
    {
      path: 'grid-system',
      name: 'Grid System',
      component: GridSystem
    },
    {
      path: 'panels',
      name: 'Panels',
      component: Panels
    },
    {
      path: 'sweet-alert',
      name: 'Sweet Alert',
      component: SweetAlert
    },
    {
      path: 'notifications',
      name: 'Notifications',
      component: Notifications
    },
    {
      path: 'icons',
      name: 'Icons',
      component: Icons
    },
    {
      path: 'typography',
      name: 'Typography',
      component: Typography
    }

  ]
}


let formsMenu = {
  path: '/forms',
  component: DashboardLayout,
  redirect: '/forms/regular',
  meta: { requiresAuth: true, requiresAdmin: false },
  children: [
    {
      path: 'regular',
      name: 'Regular Forms',
      component: RegularForms
    },
    {
      path: 'extended',
      name: 'Extended Forms',
      component: ExtendedForms
    },
    {
      path: 'validation',
      name: 'Validation Forms',
      component: ValidationForms
    },
    {
      path: 'wizard',
      name: 'Wizard',
      component: Wizard
    }
  ]
}

let tablesMenu = {
  path: '/table-list',
  component: DashboardLayout,
  redirect: '/table-list/regular',
  children: [
    {
      path: 'regular',
      name: 'Regular Tables',
      component: RegularTables
    },
    {
      path: 'extended',
      name: 'Extended Tables',
      component: ExtendedTables
    },
    {
      path: 'paginated',
      name: 'Paginated Tables',
      component: PaginatedTables
    }
  ]
}


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
  componentsMenu,
  formsMenu,
  tablesMenu,
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
        path: 'overview',
        name: 'Overview',
        component: Overview
      },
      {
        path: 'help',
        name: 'Help',
        component: Help
      },

      {
        path: 'prospects',
        name: 'Prospects',
        component: Prospects
      },
      {
        path: 'prospects_list',
        name: 'Prospect Lists',
        component: ProspectLists
      },

      {
        path: 'campaigns',
        name: 'Campaigns List',
        component: CampaignsList
      },
      {
        path: 'campaign_form',
        name: 'Campaign Form',
        component: CampaignForm
      },
      {
        path: 'campaign_edit_form',
        name: 'Campaign Edit Form',
        component: CampaignEditForm
      },

      {
        path: 'linkedin_enrichment',
        name: 'LinkedIn Enrichment',
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
        path: 'overview_standart',
        name: 'Overview standart',
        component: Overview_standart
      },
      {
        path: 'stats',
        name: 'Stats',
        component: Stats
      },
      {
        path: 'charts',
        name: 'Charts',
        component: Charts
      },
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
