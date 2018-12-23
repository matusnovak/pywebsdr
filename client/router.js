import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Listen from './views/Listen.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/listen',
      name: 'listen',
      component: Listen
    }
  ]
})
