import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store/index'

import LandingPage from '@/views/LandingPage'
import UserGuide from '@/views/UserGuide'
import CardsDisplay from '@/views/CardsDisplay'
import SessionsDisplay from '@/views/SessionsDisplay'
import * as backend from '@/api/backend'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'landingpage',
      component: LandingPage
    },
    // {
    //   path: '/upload',
    //   name: 'uploadsamples',
    //   component: UploadSamples
    // },
    {
      path: '/guide',
      name: 'UserGuide',
      component: UserGuide
    },
    {
      path: '/samples',
      name: 'samples',
      component: CardsDisplay,
      beforeEnter: (to, from, next) => {
        if (store.getters['samples/samples'].length > 0) next()
        else next({ name: 'landingpage' })
      }
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: SessionsDisplay,
      beforeEnter: (to, from, next) => {        
        if (store.getters['sessions/sessions'].length > 0) next()
        else next({ name: 'landingpage' })
      }
    },
    {
      path: '/model',
      name: 'Model',
      beforeEnter: () => {
        const backendURL = backend.setBaseURLWithDefaultOrEnvValue()
        const sessionId = store.getters['sessions/sessionId']
        window.open(`${backendURL}/session/${sessionId}/model`, '_blank')
      }  
    }
  ]
})
