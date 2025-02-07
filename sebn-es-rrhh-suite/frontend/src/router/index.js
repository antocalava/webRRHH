import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import { computed } from 'vue';

const userRoles = localStorage.getItem('rank');
const isIntern = computed(() => userRoles && userRoles.includes('xfapochizfrtv05ikicmqbb4y4ld5415jhwg7yk81fzbh6paw122sc06t6i70fpl'));
const isAdmin = computed(() => userRoles && userRoles.includes('cb88dfe7c01e300d2be5b0368f2e50895dd181601a7d31e61bfd7e597f7ef127'));
const isManager = computed(() => userRoles && userRoles.includes('38ovzt6htlz9dvkfpb6gdidjlt2zkxsue4q39wfehxlp7ykhjrp75hmk954spu0n'));
const isResponsible = computed(() => userRoles && userRoles.includes('e7698668c7a6762266de376ce96adbea6e2cc5cd203bad0adb4e1832480b784b'));

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            meta: { requiresAuth: false }
        },
        {
            path: '/trip',
            name: 'trip',
            component: () => import('../views/TripView.vue'),
            meta: { requiresAuth: true, role: 'employee' }
        },
        {
            path: '/calendar',
            name: 'calendar',
            component: () => import('../views/CalendarView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/home-office',
            name: 'home-office',
            component: () => import('../views/HomeOfficeCalendarView.vue'),
            meta: { requiresAuth: true, role: 'employee' }
        },
        {
            path: '/account',
            name: 'account',
            component: () => import('../views/Account.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/responsible',
            name: 'responsible',
            component: () => import('../views/Responsible.vue'),
            meta: { requiresAuth: true, role: 'responsible' }
        },
        {
            path: '/management',
            name: 'management',
            component: () => import('../views/Management.vue'),
            meta: { requiresAuth: true, role: 'manager' }
        },
        {
            path: '/hr/festivities',
            name: 'festivities',
            component: () => import('../views/RRHHFestivities.vue'),
            meta: { requiresAuth: true, role: 'admin' }
        },
        {
            path: '/hr/city-days',
            name: 'city-days',
            component: () => import('../views/RRHHCityDays.vue'),
            meta: { requiresAuth: true, role: 'admin' }
        },
        {
            path: '/hr/logs',
            name: 'logs',
            component: () => import('../views/RRHHLogs.vue'),
            meta: { requiresAuth: true, role: 'admin' }
        },
        {
            path: '/hr/inputs',
            name: 'inputs',
            component: () => import('../views/RRHHInputs.vue'),
            meta: { requiresAuth: true, role: 'admin' }
        },
        {
            path: '/hr/userinfo',
            name: 'user-info',
            component: () => import('../views/RRHHUserInfo.vue'),
            meta: { requiresAuth: true, role: 'admin' }
        },
        {
            path: '/hr/reporting',
            name: 'reporting',
            component: () => import('../views/RRHHReporting.vue'),
            meta: { requiresAuth: true, role: 'admin' }
        },
    ]
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('Authorization');

    // Verifica si está autenticado y pide login
    if (to.fullPath === "/login" && isAuthenticated) {
        return next('/');
    }

    // Verifica si la ruta requiere autenticación
    if (to.matched.some(route => route.meta.requiresAuth)) {
        if (!isAuthenticated) {
            return next('/login');
        }

        // Verifica los roles
        const roleRequired = to.meta.role;
        if (roleRequired) {
            if (roleRequired === 'manager' && !isManager.value) {
                return next('/');
            } else if (roleRequired === 'admin' && !isAdmin.value) {
                return next('/');
            } else if (roleRequired === 'responsible' && !isResponsible.value) {
                return next('/');
            } else if (roleRequired === 'employee' && isIntern.value) {
                return next('/');
            }
        }
    }

    // Permite el acceso si pasa todas las verificaciones
    next();
});

export default router;
