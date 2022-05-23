import Vue from 'vue'
import Vuex from 'vuex'

import sessions from '@/api/sessions'
import samples from '@/api/samples'
import datasets from '@/api/datasets'
import jobs from '@/api/jobs'
import elasticsearch from '@/api/elasticsearch'
import loading from '@/api/loading'
import pagination from '@/api/pagination'

Vue.use(Vuex)

const store = new Vuex.Store(
  {
    modules: {
      sessions: sessions.module,
      samples: samples.module,
      datasets: datasets.module,
      jobs: jobs.module,            
      elasticsearch: elasticsearch.module,
      loading: loading.module,
      pagination: pagination.module,
    },  

    state: {
      task: 'addMentions', // alternatively: 'addRelations'
      userQuery: '',
    },

    mutations: {
      setUserQuery (state, userQuery) { state.userQuery = userQuery },
    },

    actions: {},

    getters: {
      userQuery (state) { return state.userQuery },
    }
  }
)

export default store
