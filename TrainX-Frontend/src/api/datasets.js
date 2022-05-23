import Vue from 'vue'
import * as backend from '@/api/backend'
import { ApiFeedback } from '@/models/apiFeedback'

const datasets_container = {
  module: {
		namespaced: true,

		state: {
      apiFeedback: {},
    },

    getters: {},

    mutations: {
      setApiFeedback (state, apiFeedback) { state.apiFeedback = apiFeedback },
    },

    actions: {
      async postDataset (context, payload) {
        context.commit('loading/setLoading', true, { root: true })
        const response = await datasets_container.api.postDataset(payload)
        context.commit('loading/setLoading', false, { root: true })
        context.commit('setApiFeedback', response)
        await context.dispatch('sessions/getSession', context.rootGetters['sessions/sessionId'], { root: true })
      },
    }
  },

  api: {
    apiFeedback: function (response) {
			return datasets_container.parser.instantiateApiFeedback(response)
    },

    postDataset: async function (payload) {
      const response = await backend.post(`session/${payload.session_id}/uploadDataset`, payload.dataset)
      return datasets_container.api.apiFeedback(response)
    },
  },

  parser: {
    instantiateApiFeedback: function (response) {
			return new ApiFeedback(response.method, response.url, response.status)
    },
  }
}

export default datasets_container