import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home.vue'
import recordhome from '@/components/routehome/recordhome.vue'
import recordRobot from '@/components/routehome/recordRobot.vue'
import TestReplay from '@/components/routehome/TestReplay.vue'
import EditScript from '@/components/routehome/EditScript.vue'
import Monkey from '@/components/routehome/Monkey.vue'
import Report from "../components/routehome/Report.vue";
import Login from "../components/Login.vue"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
    {
      path: '/recordhome',
      name: 'recordhome',
      component: recordhome,
      children: [
        {
          path: '/recordRobot',
          name: 'recordRobot',
          component: recordRobot
        },
        {
          path: '/TestReplay',
          name: 'TestReplay',
          component: TestReplay
        },
        {
          path: '/EditScript',
          name: 'EditScript',
          component: EditScript
        },
        {
          path: '/Monkey',
          name: 'Monkey',
          component: Monkey
        }
      ]
    },
  ]
})
