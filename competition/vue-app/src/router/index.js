import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
import GroupView from "@/views/GroupView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'index',
    component: () => import('../views/StatisticsView.vue'),
    meta: {
      hasPermission: () => {return true},
      title: `${process.env.VUE_APP_TITLE} - Statistics`
    }
  },
  {
    path: '/queueUp',
    name: 'queueUp',
    component: () => import('../views/QueueUpView.vue'),
    meta: {
      hasPermission: () => {return store.getters.is_group},
      title: `${process.env.VUE_APP_TITLE} - Queue up`
    }
  },
    {
    path: '/queue',
    name: 'queue',
    component: () => import('../views/QueueView.vue'),
    meta: {
      hasPermission: () => {return true},
      title: `${process.env.VUE_APP_TITLE} - Queue`
    }
  },
  {
    path: '/live',
    name: 'liverunners',
    component: () => import('../views/LiveRunners.vue'),
    meta: {
      hasPermission: () => {return true},
      title: `${process.env.VUE_APP_TITLE} - Live`
    }
  },
  {
    path: '/control',
    name: 'control',
    component: () => import('../views/ControlView.vue'),
    meta: {
      hasPermission: () => {return store.getters.is_admin},
      title: `${process.env.VUE_APP_TITLE} - Control`
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: {
      hasPermission: () => {return true},
      title: `${process.env.VUE_APP_TITLE} - Login`
    }
  },
  {
    path: '/query',
    name: 'query',
    component: () => import('../views/QueryView'),
    meta: {
      hasPermission: () => {return store.getters.is_admin},
      title: `${process.env.VUE_APP_TITLE} - Query`
    }
  },
  {
    path: '/group',
    name: 'group',
    component: GroupView,
    meta: {
      hasPermission: () => {
        // Define the logic to check if the user has the necessary permissions
        return true; // Replace with actual permission check
      },
    }
  }
];


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.hasPermission()) next();
  else next({name: 'login', query: {'status': store.getters.isAuthenticated ? 403 : 401}});
});

export default router
